#!/usr/bin/env python3
"""
Data Pipeline Builder - ETL pipelines without code

Usage:
    python pipeline.py create --name sync-users --source postgres --destination sheets
    python pipeline.py run --name sync-users
    python pipeline.py schedule --name sync-users --cron "0 * * * *"
"""

import os
import sys
import json
import csv
import time
import hashlib
import sqlite3
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class SourceType(Enum):
    POSTGRES = "postgres"
    MYSQL = "mysql"
    MONGODB = "mongodb"
    SQLITE = "sqlite"
    GOOGLE_SHEETS = "sheets"
    AIRTABLE = "airtable"
    NOTION = "notion"
    REST_API = "api"
    GRAPHQL = "graphql"
    CSV = "csv"
    JSON = "json"
    S3 = "s3"
    GCS = "gcs"


class DestType(Enum):
    POSTGRES = "postgres"
    MYSQL = "mysql"
    MONGODB = "mongodb"
    SQLITE = "sqlite"
    GOOGLE_SHEETS = "sheets"
    AIRTABLE = "airtable"
    NOTION = "notion"
    WEBHOOK = "webhook"
    EMAIL = "email"
    SLACK = "slack"
    CSV = "csv"
    JSON = "json"


class TransformType(Enum):
    FILTER = "filter"
    MAP = "map"
    AGGREGATE = "aggregate"
    JOIN = "join"
    ENRICH = "enrich"
    CLEAN = "clean"
    VALIDATE = "validate"


@dataclass
class Pipeline:
    """Data pipeline configuration."""
    
    name: str
    source: Dict
    destination: Dict
    transformations: List[Dict] = field(default_factory=list)
    schedule: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    last_run: Optional[float] = None
    runs: List[Dict] = field(default_factory=list)


class DataPipeline:
    """Build and execute ETL pipelines."""
    
    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = Path(config_dir or Path.home() / ".data-pipeline")
        self.pipelines_dir = self.config_dir / "pipelines"
        self.logs_dir = self.config_dir / "logs"
        
        self._ensure_dirs()
    
    def _ensure_dirs(self):
        """Create necessary directories."""
        for d in [self.config_dir, self.pipelines_dir, self.logs_dir]:
            d.mkdir(parents=True, exist_ok=True)
    
    def create_pipeline(self, name: str, source: Dict, destination: Dict) -> Pipeline:
        """Create a new pipeline."""
        
        pipeline = Pipeline(
            name=name,
            source=source,
            destination=destination,
        )
        
        # Save pipeline
        pipeline_file = self.pipelines_dir / f"{name}.json"
        pipeline_file.write_text(json.dumps(pipeline.__dict__, indent=2))
        
        print(f"✓ Created pipeline: {name}")
        print(f"  Source: {source.get('type')}")
        print(f"  Destination: {destination.get('type')}")
        
        return pipeline
    
    def load_pipeline(self, name: str) -> Optional[Pipeline]:
        """Load a pipeline by name."""
        
        pipeline_file = self.pipelines_dir / f"{name}.json"
        
        if not pipeline_file.exists():
            return None
        
        data = json.loads(pipeline_file.read_text())
        return Pipeline(**data)
    
    def add_transform(self, name: str, transform: Dict) -> bool:
        """Add transformation to pipeline."""
        
        pipeline = self.load_pipeline(name)
        if not pipeline:
            print(f"✗ Pipeline not found: {name}")
            return False
        
        pipeline.transformations.append(transform)
        
        # Save updated pipeline
        pipeline_file = self.pipelines_dir / f"{name}.json"
        pipeline_file.write_text(json.dumps(pipeline.__dict__, indent=2))
        
        print(f"✓ Added transform: {transform.get('type')}")
        return True
    
    def run_pipeline(self, name: str, dry_run: bool = False, limit: Optional[int] = None) -> Dict:
        """Execute a pipeline."""
        
        pipeline = self.load_pipeline(name)
        if not pipeline:
            return {"error": f"Pipeline not found: {name}"}
        
        start_time = time.time()
        run_log = {
            "pipeline": name,
            "started_at": datetime.now().isoformat(),
            "status": "running",
            "records_processed": 0,
            "errors": [],
        }
        
        try:
            # Extract
            print(f"  Extracting from {pipeline.source.get('type')}...")
            data = self._extract(pipeline.source, limit=limit)
            run_log["extracted"] = len(data)
            print(f"    Extracted {len(data)} records")
            
            if dry_run:
                print(f"  [DRY RUN] Would transform and load {len(data)} records")
                run_log["status"] = "dry_run"
                run_log["records_processed"] = len(data)
                return run_log
            
            # Transform
            for transform in pipeline.transformations:
                print(f"  Transforming: {transform.get('type')}...")
                data = self._transform(data, transform)
            
            run_log["transformed"] = len(data)
            print(f"    Transformed to {len(data)} records")
            
            # Load
            print(f"  Loading to {pipeline.destination.get('type')}...")
            loaded = self._load(data, pipeline.destination)
            
            run_log["loaded"] = loaded
            run_log["records_processed"] = len(data)
            run_log["status"] = "success"
            
            print(f"✓ Pipeline completed: {loaded} records loaded")
            
        except Exception as e:
            run_log["status"] = "error"
            run_log["errors"].append(str(e))
            print(f"✗ Pipeline failed: {e}")
        
        finally:
            elapsed = time.time() - start_time
            run_log["elapsed_seconds"] = elapsed
            run_log["completed_at"] = datetime.now().isoformat()
            
            # Update pipeline
            pipeline.last_run = time.time()
            pipeline.runs.append(run_log)
            
            pipeline_file = self.pipelines_dir / f"{name}.json"
            pipeline_file.write_text(json.dumps(pipeline.__dict__, indent=2))
            
            # Save run log
            log_file = self.logs_dir / f"{name}_{int(start_time)}.json"
            log_file.write_text(json.dumps(run_log, indent=2))
        
        return run_log
    
    def _extract(self, source: Dict, limit: Optional[int] = None) -> List[Dict]:
        """Extract data from source."""
        
        source_type = source.get("type")
        
        if source_type == "csv":
            return self._extract_csv(source, limit)
        elif source_type == "json":
            return self._extract_json(source, limit)
        elif source_type == "api":
            return self._extract_api(source, limit)
        elif source_type == "sqlite":
            return self._extract_sqlite(source, limit)
        else:
            raise ValueError(f"Unsupported source type: {source_type}")
    
    def _extract_csv(self, source: Dict, limit: Optional[int]) -> List[Dict]:
        """Extract from CSV file."""
        
        file_path = source.get("file")
        if not file_path:
            raise ValueError("CSV source requires 'file' parameter")
        
        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if limit and i >= limit:
                    break
                data.append(row)
        
        return data
    
    def _extract_json(self, source: Dict, limit: Optional[int]) -> List[Dict]:
        """Extract from JSON file."""
        
        file_path = source.get("file")
        if not file_path:
            raise ValueError("JSON source requires 'file' parameter")
        
        content = json.loads(Path(file_path).read_text())
        
        # Handle array or object with data key
        if isinstance(content, list):
            data = content
        elif isinstance(content, dict) and "data" in content:
            data = content["data"]
        else:
            data = [content]
        
        if limit:
            data = data[:limit]
        
        return data
    
    def _extract_api(self, source: Dict, limit: Optional[int]) -> List[Dict]:
        """Extract from REST API."""
        
        url = source.get("url") or source.get("endpoint")
        if not url:
            raise ValueError("API source requires 'url' or 'endpoint' parameter")
        
        headers = source.get("headers", {})
        
        # Handle auth
        if source.get("auth") == "bearer":
            headers["Authorization"] = f"Bearer {source.get('token')}"
        elif source.get("auth") == "api_key":
            key_name = source.get("key_name", "X-API-Key")
            headers[key_name] = source.get("api_key")
        
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req, timeout=30)
        content = json.loads(response.read().decode('utf-8'))
        
        if isinstance(content, list):
            data = content
        elif isinstance(content, dict) and "data" in content:
            data = content["data"]
        else:
            data = [content]
        
        if limit:
            data = data[:limit]
        
        return data
    
    def _extract_sqlite(self, source: Dict, limit: Optional[int]) -> List[Dict]:
        """Extract from SQLite database."""
        
        db_path = source.get("database")
        query = source.get("query")
        
        if not db_path or not query:
            raise ValueError("SQLite source requires 'database' and 'query' parameters")
        
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        data = [dict(row) for row in rows]
        
        if limit:
            data = data[:limit]
        
        conn.close()
        return data
    
    def _transform(self, data: List[Dict], transform: Dict) -> List[Dict]:
        """Apply transformation to data."""
        
        transform_type = transform.get("type")
        
        if transform_type == "filter":
            return self._transform_filter(data, transform)
        elif transform_type == "map":
            return self._transform_map(data, transform)
        elif transform_type == "clean":
            return self._transform_clean(data, transform)
        elif transform_type == "aggregate":
            return self._transform_aggregate(data, transform)
        else:
            # Unknown transform, return as-is
            return data
    
    def _transform_filter(self, data: List[Dict], transform: Dict) -> List[Dict]:
        """Filter rows by condition."""
        
        field = transform.get("field")
        value = transform.get("value")
        operator = transform.get("operator", "eq")
        
        result = []
        for row in data:
            row_value = row.get(field)
            
            if operator == "eq" and row_value == value:
                result.append(row)
            elif operator == "neq" and row_value != value:
                result.append(row)
            elif operator == "gt" and row_value > value:
                result.append(row)
            elif operator == "lt" and row_value < value:
                result.append(row)
            elif operator == "contains" and value in str(row_value):
                result.append(row)
            elif operator == "exists" and row_value is not None:
                result.append(row)
        
        return result
    
    def _transform_map(self, data: List[Dict], transform: Dict) -> List[Dict]:
        """Map field names."""
        
        from_field = transform.get("from")
        to_field = transform.get("to")
        mapping = transform.get("mapping", {})
        
        result = []
        for row in data:
            new_row = row.copy()
            
            if from_field and to_field:
                # Single field rename
                if from_field in new_row:
                    new_row[to_field] = new_row.pop(from_field)
            elif mapping:
                # Multiple field mapping
                for old_name, new_name in mapping.items():
                    if old_name in new_row:
                        new_row[new_name] = new_row.pop(old_name)
            
            result.append(new_row)
        
        return result
    
    def _transform_clean(self, data: List[Dict], transform: Dict) -> List[Dict]:
        """Clean data (nulls, whitespace)."""
        
        result = []
        for row in data:
            new_row = {}
            for key, value in row.items():
                # Handle None/null
                if value is None:
                    if transform.get("remove_nulls"):
                        continue
                    new_row[key] = transform.get("null_default", "")
                # Handle strings
                elif isinstance(value, str):
                    new_row[key] = value.strip()
                    if transform.get("lowercase"):
                        new_row[key] = new_row[key].lower()
                else:
                    new_row[key] = value
            result.append(new_row)
        
        return result
    
    def _transform_aggregate(self, data: List[Dict], transform: Dict) -> List[Dict]:
        """Aggregate data."""
        
        group_by = transform.get("group_by", [])
        aggregations = transform.get("aggregations", {})
        
        if not group_by:
            # Aggregate all
            result = {}
            for field, agg_type in aggregations.items():
                values = [row.get(field) for row in data if row.get(field) is not None]
                
                if agg_type == "sum":
                    result[f"{field}_sum"] = sum(values)
                elif agg_type == "avg":
                    result[f"{field}_avg"] = sum(values) / len(values) if values else 0
                elif agg_type == "count":
                    result[f"{field}_count"] = len(values)
                elif agg_type == "min":
                    result[f"{field}_min"] = min(values) if values else None
                elif agg_type == "max":
                    result[f"{field}_max"] = max(values) if values else None
            
            return [result]
        
        # Group by fields
        groups = {}
        for row in data:
            key = tuple(row.get(field) for field in group_by)
            if key not in groups:
                groups[key] = []
            groups[key].append(row)
        
        result = []
        for key, rows in groups.items():
            agg_row = dict(zip(group_by, key))
            
            for field, agg_type in aggregations.items():
                values = [row.get(field) for row in rows if row.get(field) is not None]
                
                if agg_type == "sum":
                    agg_row[f"{field}_sum"] = sum(values)
                elif agg_type == "avg":
                    agg_row[f"{field}_avg"] = sum(values) / len(values) if values else 0
                elif agg_type == "count":
                    agg_row[f"{field}_count"] = len(values)
                elif agg_type == "min":
                    agg_row[f"{field}_min"] = min(values) if values else None
                elif agg_type == "max":
                    agg_row[f"{field}_max"] = max(values) if values else None
            
            result.append(agg_row)
        
        return result
    
    def _load(self, data: List[Dict], destination: Dict) -> int:
        """Load data to destination."""
        
        dest_type = destination.get("type")
        
        if dest_type == "csv":
            return self._load_csv(data, destination)
        elif dest_type == "json":
            return self._load_json(data, destination)
        elif dest_type == "webhook":
            return self._load_webhook(data, destination)
        elif dest_type == "sqlite":
            return self._load_sqlite(data, destination)
        else:
            raise ValueError(f"Unsupported destination type: {dest_type}")
    
    def _load_csv(self, data: List[Dict], destination: Dict) -> int:
        """Load to CSV file."""
        
        file_path = destination.get("file")
        if not file_path:
            raise ValueError("CSV destination requires 'file' parameter")
        
        if not data:
            return 0
        
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        
        return len(data)
    
    def _load_json(self, data: List[Dict], destination: Dict) -> int:
        """Load to JSON file."""
        
        file_path = destination.get("file")
        if not file_path:
            raise ValueError("JSON destination requires 'file' parameter")
        
        Path(file_path).write_text(json.dumps(data, indent=2))
        return len(data)
    
    def _load_webhook(self, data: List[Dict], destination: Dict) -> int:
        """Send to webhook."""
        
        url = destination.get("url")
        if not url:
            raise ValueError("Webhook destination requires 'url' parameter")
        
        headers = {"Content-Type": "application/json"}
        if destination.get("auth") == "bearer":
            headers["Authorization"] = f"Bearer {destination.get('token')}"
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        response = urllib.request.urlopen(req, timeout=30)
        return len(data)
    
    def _load_sqlite(self, data: List[Dict], destination: Dict) -> int:
        """Load to SQLite database."""
        
        db_path = destination.get("database")
        table = destination.get("table")
        
        if not db_path or not table:
            raise ValueError("SQLite destination requires 'database' and 'table' parameters")
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        if data:
            # Create table if not exists
            columns = data[0].keys()
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} ({', '.join(columns)})")
            
            # Insert data
            placeholders = ', '.join(['?' for _ in columns])
            cursor.executemany(
                f"INSERT INTO {table} VALUES ({placeholders})",
                [tuple(row.get(col) for col in columns) for row in data]
            )
            
            conn.commit()
        
        conn.close()
        return len(data)
    
    def list_pipelines(self) -> List[Dict]:
        """List all pipelines."""
        
        pipelines = []
        
        for pipeline_file in self.pipelines_dir.glob("*.json"):
            try:
                data = json.loads(pipeline_file.read_text())
                pipelines.append({
                    "name": data.get("name"),
                    "source": data.get("source", {}).get("type"),
                    "destination": data.get("destination", {}).get("type"),
                    "transforms": len(data.get("transformations", [])),
                    "last_run": data.get("last_run"),
                })
            except:
                continue
        
        return pipelines
    
    def get_status(self, name: str) -> Dict:
        """Get pipeline status."""
        
        pipeline = self.load_pipeline(name)
        if not pipeline:
            return {"error": f"Pipeline not found: {name}"}
        
        return {
            "name": pipeline.name,
            "source": pipeline.source,
            "destination": pipeline.destination,
            "transforms": len(pipeline.transformations),
            "schedule": pipeline.schedule,
            "last_run": pipeline.last_run,
            "total_runs": len(pipeline.runs),
            "last_status": pipeline.runs[-1].get("status") if pipeline.runs else None,
        }


def main():
    """CLI entry point."""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Data Pipeline Builder")
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # create command
    create_parser = subparsers.add_parser('create', help='Create pipeline')
    create_parser.add_argument('--name', required=True, help='Pipeline name')
    create_parser.add_argument('--source', required=True, help='Source type')
    create_parser.add_argument('--destination', required=True, help='Destination type')
    
    # extract command
    extract_parser = subparsers.add_parser('extract', help='Configure extraction')
    extract_parser.add_argument('--pipeline', required=True, help='Pipeline name')
    
    # transform command
    transform_parser = subparsers.add_parser('transform', help='Add transformation')
    transform_parser.add_argument('--pipeline', required=True, help='Pipeline name')
    transform_parser.add_argument('--type', required=True, help='Transform type')
    transform_parser.add_argument('--field', help='Field name')
    transform_parser.add_argument('--value', help='Field value')
    
    # load command
    load_parser = subparsers.add_parser('load', help='Configure load')
    load_parser.add_argument('--pipeline', required=True, help='Pipeline name')
    load_parser.add_argument('--mode', default='append', help='Load mode')
    
    # run command
    run_parser = subparsers.add_parser('run', help='Run pipeline')
    run_parser.add_argument('--name', required=True, help='Pipeline name')
    run_parser.add_argument('--dry-run', action='store_true', help='Dry run')
    run_parser.add_argument('--limit', type=int, help='Limit records')
    
    # list command
    list_parser = subparsers.add_parser('list', help='List pipelines')
    
    # status command
    status_parser = subparsers.add_parser('status', help='Get pipeline status')
    status_parser.add_argument('--name', required=True, help='Pipeline name')
    
    args = parser.parse_args()
    
    pipeline = DataPipeline()
    
    if args.command == 'create':
        pipeline.create_pipeline(
            name=args.name,
            source={"type": args.source},
            destination={"type": args.destination}
        )
    
    elif args.command == 'transform':
        transform = {"type": args.type}
        if args.field:
            transform["field"] = args.field
        if args.value:
            transform["value"] = args.value
        
        pipeline.add_transform(args.pipeline, transform)
    
    elif args.command == 'run':
        result = pipeline.run_pipeline(
            name=args.name,
            dry_run=args.dry_run,
            limit=args.limit
        )
        print(json.dumps(result, indent=2))
    
    elif args.command == 'list':
        pipelines = pipeline.list_pipelines()
        print(f"\nFound {len(pipelines)} pipelines:\n")
        for p in pipelines:
            print(f"  {p['name']}")
            print(f"    Source: {p['source']} → Destination: {p['destination']}")
            print(f"    Transforms: {p['transforms']}, Last run: {p['last_run']}")
            print()
    
    elif args.command == 'status':
        status = pipeline.get_status(args.name)
        print(json.dumps(status, indent=2))
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()