import argparse
import contextlib
import importlib.util
import io
import json
import pathlib
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


SCRIPT = pathlib.Path(__file__).parents[1] / "scripts" / "odata_get.py"
SPEC = importlib.util.spec_from_file_location("odata_get", SCRIPT)
odata_get = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(odata_get)


class PagingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if "$skiptoken=next" in self.path:
            payload = {"value": [{"Id": 3}]}
        else:
            payload = {
                "value": [{"Id": 1}, {"Id": 2}],
                "@odata.nextLink": "/odata/People?$skiptoken=next",
            }
        body = json.dumps(payload).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return


class ODataGetTests(unittest.TestCase):
    def test_metadata_summary_preserves_types_and_annotation_values(self):
        xml = b"""<?xml version='1.0'?>
        <edmx:Edmx xmlns:edmx='http://docs.oasis-open.org/odata/ns/edmx' xmlns='http://docs.oasis-open.org/odata/ns/edm'>
          <edmx:DataServices><Schema Namespace='Demo'>
            <EnumType Name='State'><Member Name='Open' Value='1'/></EnumType>
            <EntityType Name='Thing'><Key><PropertyRef Name='Id'/></Key><Property Name='Id' Type='Edm.Int32' Nullable='false'/></EntityType>
            <EntityContainer Name='Default'><EntitySet Name='Things' EntityType='Demo.Thing'/></EntityContainer>
            <Annotations Target='Demo.Default/Things'><Annotation Term='Org.OData.Capabilities.V1.TopSupported' Bool='false'/></Annotations>
          </Schema></edmx:DataServices>
        </edmx:Edmx>"""
        result = odata_get.summarize_metadata(xml)
        self.assertEqual(result["types"][0]["members"][0]["name"], "Open")
        self.assertEqual(result["types"][1]["keys"], ["Id"])
        self.assertEqual(result["annotations"][0]["value"], "false")

    def test_query_options_are_not_duplicated(self):
        args = argparse.Namespace(
            select="Id,Name",
            filter=None,
            orderby=None,
            top=5,
            skip=None,
            count=None,
            expand=None,
            search=None,
            query=["$apply=groupby((Category))"],
        )
        self.assertEqual(
            odata_get.query_pairs(args),
            [("$select", "Id,Name"), ("$top", "5"), ("$apply", "groupby((Category))")],
        )

    def test_error_detail_uses_odata_code_and_message(self):
        body = json.dumps({"error": {"code": "BadQuery", "message": "Unknown property"}}).encode()
        self.assertEqual(
            odata_get.error_detail(body, "application/json"),
            "BadQuery: Unknown property",
        )

    def test_server_driven_paging_follows_relative_next_link(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), PagingHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        args = argparse.Namespace(
            service_root=f"http://127.0.0.1:{server.server_port}/odata",
            resource="People",
            odata_version="4.0",
            bearer_env=None,
            basic_user_env=None,
            basic_password_env=None,
            header_env=[],
            timeout=2.0,
            output=None,
            select=None,
            filter=None,
            orderby=None,
            top=None,
            skip=None,
            count=None,
            expand=None,
            search=None,
            query=[],
            all_pages=True,
            max_pages=5,
            max_items=10,
        )
        output = io.StringIO()
        try:
            with contextlib.redirect_stdout(output):
                odata_get.command_get(args)
        finally:
            server.shutdown()
            server.server_close()
        result = json.loads(output.getvalue())
        self.assertEqual([item["Id"] for item in result["value"]], [1, 2, 3])
        self.assertEqual(result["_retrieval"], {"pages": 2, "items": 3, "truncated": False})


if __name__ == "__main__":
    unittest.main()
