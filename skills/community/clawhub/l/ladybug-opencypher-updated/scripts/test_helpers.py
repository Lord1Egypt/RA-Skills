#!/usr/bin/env python3
"""Integration smoke tests using temporary databases and the selected interpreter."""
import asyncio
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import ladybug as lb

SCRIPTS = Path(__file__).resolve().parent


class HelperTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="ladybug-skill-test-")
        self.addCleanup(self.temp.cleanup)
        self.db = Path(self.temp.name) / "test.lbdb"

    def run_query(self, query, *options):
        return subprocess.run([sys.executable, str(SCRIPTS / "run_cypher.py"),
                               str(self.db), "-c", query, *options],
                              capture_output=True, text=True, timeout=45)

    def seed(self):
        result = self.run_query("CREATE NODE TABLE Paper(id STRING PRIMARY KEY, title STRING);"
                                "CREATE (:Paper {id:'a',title:'A'});"
                                "CREATE (:Paper {id:'b',title:'B'});"
                                "CREATE (:Paper {id:'c',title:'C'});", "--write", "--create")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_environment(self):
        result = subprocess.run([sys.executable, str(SCRIPTS / "check_env.py"), "--smoke"],
                                capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("0.21.2", result.stdout)

    def test_missing_database_and_creation_scope(self):
        self.assertNotEqual(self.run_query("RETURN 1").returncode, 0)
        self.assertFalse(self.db.exists())
        self.assertNotEqual(self.run_query("RETURN 1", "--create").returncode, 0)
        self.assertFalse(self.db.exists())
        self.seed()
        self.assertNotEqual(self.run_query("RETURN 1", "--write", "--create").returncode, 0)

    def test_read_only_rejects_delete_and_preserves_records(self):
        self.seed()
        rejected = self.run_query("MATCH (p:Paper) DELETE p")
        self.assertNotEqual(rejected.returncode, 0)
        result = self.run_query("MATCH (p:Paper) RETURN COUNT(*)", "--print-rows")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("[3]", result.stdout)

    def test_parameters_are_values_not_cypher(self):
        self.seed()
        title = "O'Brien'); MATCH (p:Paper) DELETE p; //"
        result = self.run_query("MATCH (p:Paper {id:$id}) SET p.title=$title RETURN p.title",
                                "--write", "--params", json.dumps({"id":"a", "title":title}), "--print-rows")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(title, result.stdout)
        verify = self.run_query("MATCH (p:Paper) RETURN COUNT(*)", "--print-rows")
        self.assertIn("[3]", verify.stdout)

    def test_relationship_identity_direction_and_multiplicity(self):
        self.seed()
        result = self.run_query("CREATE REL TABLE CITES(FROM Paper TO Paper, evidence STRING);"
             "CREATE REL TABLE EXTENDS(FROM Paper TO Paper, evidence STRING);"
             "MATCH (a:Paper {id:'a'}),(b:Paper {id:'b'}) CREATE (a)-[:CITES {evidence:'e1'}]->(b);"
             "MATCH (a:Paper {id:'a'}),(b:Paper {id:'b'}) CREATE (a)-[:CITES {evidence:'e2'}]->(b);"
             "MATCH (a:Paper {id:'a'}),(b:Paper {id:'b'}) CREATE (a)-[:EXTENDS {evidence:'e3'}]->(b);", "--write")
        self.assertEqual(result.returncode, 0, result.stderr)
        verify = self.run_query("MATCH (a:Paper)-[r]->(b:Paper) RETURN a.id,label(r),r.evidence,b.id ORDER BY r.evidence", "--print-rows")
        self.assertEqual(verify.returncode, 0, verify.stderr)
        for relation, evidence in [("CITES","e1"),("CITES","e2"),("EXTENDS","e3")]:
            self.assertIn(json.dumps(["a",relation,evidence,"b"]), verify.stdout)
        self.assertIn("3 row(s)", verify.stdout)

    def test_explicit_transaction_rolls_back_on_failure(self):
        self.seed()
        failed = self.run_query("BEGIN TRANSACTION; CREATE (:Paper {id:'d',title:'D'});"
                                "MATCH (x:MissingTable) RETURN x; COMMIT;", "--write")
        self.assertNotEqual(failed.returncode, 0)
        result = self.run_query("MATCH (p:Paper) RETURN COUNT(*)", "--print-rows")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("[3]", result.stdout)

    def test_bounded_preview_and_multistatement_results(self):
        self.seed()
        result = self.run_query("MATCH (p:Paper) RETURN p.id ORDER BY p.id; RETURN 42;",
                                "--print-rows", "--max-rows", "2")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("preview truncated to 2 of 3", result.stdout)
        self.assertIn("statement[1]: 1 row(s)", result.stdout)
        self.assertNotIn('["c"]', result.stdout)

    def test_query_and_parameter_files(self):
        self.seed()
        query = Path(self.temp.name)/"query.cypher"
        params = Path(self.temp.name)/"params.json"
        query.write_text("MATCH (p:Paper {id:$id}) RETURN p.title", encoding="utf-8")
        params.write_text('{"id":"b"}', encoding="utf-8")
        result = subprocess.run([sys.executable,str(SCRIPTS/"run_cypher.py"),str(self.db),
                 "--file",str(query),"--params-file",str(params),"--print-rows"],capture_output=True,text=True,timeout=45)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('["B"]',result.stdout)

    def test_async_api(self):
        async def run():
            db = lb.Database(":memory:", buffer_pool_size=256*1024*1024)
            conn = lb.AsyncConnection(db, max_concurrent_queries=2)
            try:
                result = await conn.execute("RETURN $value", parameters={"value":42})
                try:
                    self.assertEqual(result.get_next(), [42])
                finally:
                    result.close()
            finally:
                conn.close()
                db.close()
        asyncio.run(run())


if __name__ == "__main__":
    unittest.main(verbosity=2)
