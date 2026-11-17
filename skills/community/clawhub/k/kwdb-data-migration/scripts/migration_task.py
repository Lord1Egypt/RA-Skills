"""
migration_task.py - Complete Migration Workflow Orchestrator

Provides end-to-end migration workflow management by composing KDTS API calls.
Handles all migration phases from connection testing through completion monitoring.

Supported workflows:
1. Full Migration (Schema + Data)
2. Schema-Only Migration (DDL only)
3. Data-Only Migration (tables must exist)
4. Table-Level Migration (for restricted sources)

Task states (from KDTS API): SUBMITTED, RUNNING, SUCCEEDED, FAILED, KILLED

IMPORTANT: KDTS API only supports KILL and QUERY actions - NO pause/resume.
"""

from typing import Dict, Any, List, Optional, Callable
from enum import Enum
import time
import logging

# Import DataSourceManager for engine detection
try:
    from .data_source import DataSourceManager
except ImportError:
    from data_source import DataSourceManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


class MigrationWorkflow(str, Enum):
    """Supported migration workflows."""
    FULL_MIGRATION = "full_migration"
    SCHEMA_ONLY = "schema_only"
    DATA_ONLY = "data_only"
    TABLE_LEVEL = "table_level"


class MigrationStep(str, Enum):
    """Migration workflow steps."""
    TEST_CONNECTIONS = "test_connections"
    VALIDATE_CONFIG = "validate_config"
    READ_METADATA = "read_metadata"
    PREVIEW_DDL = "preview_ddl"
    EXECUTE_DDL = "execute_ddl"
    BUILD_SCRIPT = "build_script"
    EXECUTE_MIGRATION = "execute_migration"
    MONITOR_PROGRESS = "monitor_progress"


class MigrationStatus(str, Enum):
    """Migration task status (from KDTS API)."""
    SUBMITTED = "SUBMITTED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    KILLED = "KILLED"
    UNKNOWN = "UNKNOWN"


class MigrationWorkflowManager:
    """
    Complete migration workflow manager.

    Orchestrates the full migration lifecycle by composing
    calls to KDTS API client. Handles errors, retries, and
    provides progress tracking.
    """

    # Final statuses that indicate workflow completion
    FINAL_STATUSES = {MigrationStatus.SUCCEEDED, MigrationStatus.FAILED, MigrationStatus.KILLED}

    def __init__(self, api_client=None):
        """
        Initialize MigrationWorkflowManager.

        Args:
            api_client: KDTS API client instance (from scripts/api_client.py)
        """
        self.api_client = api_client
        self._workflow_history: List[Dict[str, Any]] = []
        self._current_step: Optional[MigrationStep] = None

    def _require_api_client(self):
        """Validate that API client is available."""
        if not self.api_client:
            raise ValueError(
                "API client is required. Initialize with: "
                "MigrationWorkflowManager(api_client=KDTSClient(base_url='...'))"
            )

    # ==================== Connection Testing ====================

    def test_connections(
        self,
        source_config: Dict[str, Any],
        target_config: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Test both source and target connections.

        Args:
            source_config: Source database configuration
            target_config: Target database configuration (KAIWUDB)

        Returns:
            Test result with source/target status
        """
        self._require_api_client()
        self._current_step = MigrationStep.TEST_CONNECTIONS

        logger.info("Testing source connection...")
        source_result = self.api_client.test_connection(source_config, is_target=False)

        logger.info("Testing target connection...")
        target_result = self.api_client.test_connection(target_config, is_target=True)

        result = {
            "step": MigrationStep.TEST_CONNECTIONS.value,
            "source": source_result,
            "target": target_result,
            "source_ok": source_result.get("code") == 0,
            "target_ok": target_result.get("code") == 0,
            "all_ok": source_result.get("code") == 0 and target_result.get("code") == 0,
        }

        self._workflow_history.append(result)
        return result

    # ==================== Metadata Reading ====================

    def read_source_metadata(
        self,
        source_config: Dict[str, Any],
        metadata_options: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Read source database metadata.

        Args:
            source_config: Source database configuration (must include dbName)
            metadata_options: Metadata extraction options

        Returns:
            Metadata reading result with database info
        """
        self._require_api_client()
        self._current_step = MigrationStep.READ_METADATA

        logger.info(f"Reading metadata from {source_config.get('type')}:{source_config.get('dbName')}...")
        result = self.api_client.read_metadata(source_config, metadata_options)

        result["step"] = MigrationStep.READ_METADATA.value
        self._workflow_history.append(result)

        return result

    # ==================== DDL Operations ====================

    def preview_ddl(
        self,
        target_config: Dict[str, Any],
        source_db: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
        is_time_series: bool = False,
    ) -> Dict[str, Any]:
        """
        Preview DDL for target KaiwuDB.

        Args:
            target_config: Target KAIWUDB configuration
            source_db: Full source database object from read_metadata
            metadata: Metadata configuration
            is_time_series: Whether source is time-series data

        Returns:
            DDL preview result
        """
        self._require_api_client()
        self._current_step = MigrationStep.PREVIEW_DDL

        logger.info("Previewing DDL for target...")
        result = self.api_client.preview_ddl(
            target_config, source_db, metadata, is_time_series
        )

        result["step"] = MigrationStep.PREVIEW_DDL.value
        self._workflow_history.append(result)

        return result

    def execute_ddl(
        self,
        target_config: Dict[str, Any],
        ddl_script: Dict[str, Any],
        auto_ddl: bool = True,
    ) -> Dict[str, Any]:
        """
        Execute DDL on target KaiwuDB.

        Args:
            target_config: Target KAIWUDB configuration
            ddl_script: DDL script from preview
            auto_ddl: Auto-create database and tables

        Returns:
            DDL execution result with log path
        """
        self._require_api_client()
        self._current_step = MigrationStep.EXECUTE_DDL

        logger.info("Executing DDL on target...")
        result = self.api_client.execute_ddl(target_config, ddl_script, auto_ddl)

        result["step"] = MigrationStep.EXECUTE_DDL.value
        self._workflow_history.append(result)

        return result

    # ==================== Migration Script Operations ====================

    def build_migration_script(
        self,
        source_config: Dict[str, Any],
        target_config: Dict[str, Any],
        tables: Optional[List[Dict[str, Any]]] = None,
        data_config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Build DataX migration script.

        Args:
            source_config: Source database configuration
            target_config: Target KAIWUDB configuration
            tables: Table mappings (empty for full migration)
            data_config: Data migration settings

        Returns:
            Script building result with script names
        """
        self._require_api_client()
        self._current_step = MigrationStep.BUILD_SCRIPT

        logger.info("Building migration script...")
        result = self.api_client.build_migration(
            source_config, target_config, tables, data_config
        )

        result["step"] = MigrationStep.BUILD_SCRIPT.value
        self._workflow_history.append(result)

        return result

    def execute_migration_script(
        self,
        script_names: List[str],
    ) -> Dict[str, Any]:
        """
        Execute built migration scripts.

        Args:
            script_names: List of script file names

        Returns:
            Execution result with log paths
        """
        self._require_api_client()
        self._current_step = MigrationStep.EXECUTE_MIGRATION

        logger.info(f"Executing migration: {script_names}")
        result = self.api_client.execute_migration(script_names)

        result["step"] = MigrationStep.EXECUTE_MIGRATION.value
        result["script_names"] = script_names
        self._workflow_history.append(result)

        return result

    def execute_migration_batches(
        self,
        script_names: List[str],
        batch_size: int = 10,
        batch_timeout: int = 3600,
        poll_interval: int = 2,
        on_batch_progress: Optional[Callable[[int, int, Dict[str, Any]], None]] = None,
    ) -> Dict[str, Any]:
        """
        Execute migration scripts in batches (RECOMMENDED for many tables).

        Submits scripts batch by batch (default 10 per batch) and waits for every
        script in the batch to reach a final state before submitting the next one.
        Prevents HTTP 4003 request timeouts caused by submitting dozens of scripts
        in a single request (the KDTS server starts DataX processes sequentially
        and can exceed the client read timeout).

        Args:
            script_names: List of script file names to execute
            batch_size: Number of scripts per batch (default: 10)
            batch_timeout: Max seconds to wait for one batch to finish (default: 3600)
            poll_interval: Status polling interval in seconds (default: 2)
            on_batch_progress: Optional callback (batch_index, total_batches, batch_result)

        Returns:
            Summary dict:
                {
                    "total_batches": int,
                    "completed_batches": int,
                    "all_succeeded": bool,
                    "batch_results": [ {batch, all_succeeded, final_statuses, elapsed_time} ]
                }

        Notes:
            - A 4003 timeout on submission means the request REACHED the server and
              the server keeps processing — the batch is still monitored to completion.
            - UNKNOWN status is not final: scripts still queued on the server are
              polled until they reach SUCCEEDED/FAILED/KILLED.
        """
        self._require_api_client()
        batches = [script_names[i:i + batch_size] for i in range(0, len(script_names), batch_size)]
        total_batches = len(batches)
        results = []

        for idx, batch in enumerate(batches, 1):
            logger.info(f"Executing batch {idx}/{total_batches} ({len(batch)} scripts)")
            exec_result = self.execute_migration_script(batch)
            code = exec_result.get("code")
            if code not in (0, 4003):
                # Hard submission failure (not a timeout): record and move on
                results.append({"batch": idx, "all_succeeded": False,
                                "submitted": False, "error": exec_result})
                continue
            # code 4003 = request reached the server but response timed out;
            # the server keeps processing, so still wait for final states.
            batch_status = self._wait_batch_completion(batch, batch_timeout, poll_interval)
            batch_status["batch"] = idx
            results.append(batch_status)
            if on_batch_progress:
                on_batch_progress(idx, total_batches, batch_status)

        all_succeeded = all(r.get("all_succeeded") for r in results)
        return {
            "total_batches": total_batches,
            "completed_batches": len(results),
            "all_succeeded": all_succeeded,
            "batch_results": results,
        }

    def _wait_batch_completion(self, script_names: List[str],
                               timeout: int, poll_interval: int) -> Dict[str, Any]:
        """Poll all scripts in a batch until every one reaches a final state."""
        start_time = time.time()
        final_statuses = {}
        while time.time() - start_time < timeout:
            for sn in script_names:
                if sn in final_statuses:
                    continue
                status = self.query_task_status(sn)
                st = status.get("data", {}).get("status", MigrationStatus.UNKNOWN.value)
                if st in MigrationWorkflowManager.FINAL_STATUSES:
                    final_statuses[sn] = st
            if len(final_statuses) == len(script_names):
                break
            time.sleep(poll_interval)

        all_succeeded = (len(final_statuses) == len(script_names)
                         and all(v == MigrationStatus.SUCCEEDED.value for v in final_statuses.values()))
        return {
            "all_succeeded": all_succeeded,
            "final_statuses": final_statuses,
            "elapsed_time": time.time() - start_time,
        }

    # ==================== Status Monitoring ====================

    def query_task_status(
        self,
        script_name: str,
    ) -> Dict[str, Any]:
        """
        Query migration task status.

        Args:
            script_name: Migration script name

        Returns:
            Task status with progress
        """
        self._require_api_client()
        self._current_step = MigrationStep.MONITOR_PROGRESS

        result = self.api_client.query_status(script_name)
        result["step"] = MigrationStep.MONITOR_PROGRESS.value

        return result

    def wait_for_completion(
        self,
        script_name: str,
        timeout: int = 3600,
        poll_interval: int = 2,
        on_progress: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> Dict[str, Any]:
        """
        Wait for migration task to complete.

        Args:
            script_name: Migration script name
            timeout: Maximum wait time in seconds
            poll_interval: Status check interval in seconds
            on_progress: Optional callback for progress updates

        Returns:
            Final task status
        """
        self._require_api_client()
        self._current_step = MigrationStep.MONITOR_PROGRESS

        logger.info(f"Waiting for migration to complete (timeout={timeout}s)...")
        start_time = time.time()
        last_progress = -1

        while time.time() - start_time < timeout:
            status = self.query_task_status(script_name)
            current_status = status.get("data", {}).get("status", MigrationStatus.UNKNOWN.value)
            progress = status.get("data", {}).get("progress", 0)

            # Log progress changes
            if progress != last_progress:
                logger.info(f"Status: {current_status}, Progress: {progress}%")
                last_progress = progress

            # Call progress callback if provided
            if on_progress:
                on_progress(status)

            # Check for final status
            if current_status in MigrationWorkflowManager.FINAL_STATUSES:
                result = {
                    "step": MigrationStep.MONITOR_PROGRESS.value,
                    "script_name": script_name,
                    "final_status": current_status,
                    "progress": progress,
                    "elapsed_time": time.time() - start_time,
                    "status_response": status,
                }
                self._workflow_history.append(result)
                return result

            time.sleep(poll_interval)

        # Timeout
        result = {
            "step": MigrationStep.MONITOR_PROGRESS.value,
            "script_name": script_name,
            "final_status": "TIMEOUT",
            "elapsed_time": time.time() - start_time,
            "message": f"Migration did not complete within {timeout} seconds",
        }
        self._workflow_history.append(result)
        return result

    def kill_task(
        self,
        script_name: str,
        confirm: bool = False,
    ) -> Dict[str, Any]:
        """
        Kill a running migration task.

        WARNING: This is a dangerous operation that may leave data in inconsistent state.

        Args:
            script_name: Migration script name
            confirm: Must be True to actually kill (safety guard)

        Returns:
            Kill operation result or warning if not confirmed
        """
        self._require_api_client()

        if not confirm:
            return {
                "status": "BLOCKED",
                "warning": "Killing a running migration may leave data in inconsistent state. "
                           "Please pass confirm=True to proceed.",
                "task_status": self.query_task_status(script_name).get("data", {}),
            }

        logger.warning(f"Killing migration task: {script_name}")
        result = self.api_client.control_task(script_name, action="KILL")

        result["operation"] = "KILL"
        result["step"] = MigrationStep.MONITOR_PROGRESS.value

        self._workflow_history.append(result)
        return result

    # ==================== Full Workflow Orchestration ====================

    def run_full_migration(
        self,
        source_config: Dict[str, Any],
        target_config: Dict[str, Any],
        metadata_options: Optional[Dict[str, Any]] = None,
        data_config: Optional[Dict[str, Any]] = None,
        execute_ddl_confirm: Optional[Callable[[Dict[str, Any]], bool]] = None,
        kill_confirm: bool = False,
        timeout: int = 3600,
        poll_interval: int = 2,
    ) -> Dict[str, Any]:
        """
        Run complete full migration workflow (Schema + Data).

        Args:
            source_config: Source database configuration
            target_config: Target KAIWUDB configuration
            metadata_options: Metadata extraction options
            data_config: Data migration settings
            execute_ddl_confirm: Callback to confirm DDL execution (return True to proceed)
            kill_confirm: Whether to auto-confirm kill if needed
            timeout: Overall timeout in seconds
            poll_interval: Status check interval

        Returns:
            Complete workflow result
        """
        workflow_id = f"WF_{int(time.time())}"
        logger.info(f"Starting full migration workflow: {workflow_id}")

        result = {
            "workflow_id": workflow_id,
            "workflow_type": MigrationWorkflow.FULL_MIGRATION.value,
            "start_time": time.time(),
            "steps": [],
            "success": False,
        }

        try:
            # Step 1: Test connections
            conn_result = self.test_connections(source_config, target_config)
            result["steps"].append(conn_result)

            if not conn_result["all_ok"]:
                result["error"] = "Connection test failed"
                result["end_time"] = time.time()
                return result

            # Step 2: Read source metadata
            meta_result = self.read_source_metadata(source_config, metadata_options)
            result["steps"].append(meta_result)

            if meta_result.get("code") != 0:
                result["error"] = f"Metadata reading failed: {meta_result.get('message')}"
                result["end_time"] = time.time()
                return result

            source_db = meta_result.get("data", {})

            # Step 3: Preview DDL
            # Determine if time series based on source type (auto-detect engine)
            source_type = source_config.get("type", "")
            is_time_series = (
                source_config.get("engine") == "TIMESERIES" or
                DataSourceManager.get_engine(source_type) == "TIMESERIES"
            )
            ddl_preview = self.preview_ddl(
                target_config, source_db, metadata_options,
                is_time_series=is_time_series
            )
            result["steps"].append(ddl_preview)

            if ddl_preview.get("code") != 0:
                result["error"] = f"DDL preview failed: {ddl_preview.get('message')}"
                result["end_time"] = time.time()
                return result

            # Step 4: Execute DDL (with optional confirmation)
            if execute_ddl_confirm:
                if not execute_ddl_confirm(ddl_preview):
                    result["error"] = "DDL execution not confirmed by user"
                    result["end_time"] = time.time()
                    return result

            ddl_execute = self.execute_ddl(target_config, ddl_preview.get("data", {}))
            result["steps"].append(ddl_execute)

            if ddl_execute.get("code") != 0:
                result["error"] = f"DDL execution failed: {ddl_execute.get('message')}"
                result["end_time"] = time.time()
                return result

            # Step 5: Build migration script
            build_result = self.build_migration_script(
                source_config, target_config,
                tables=[],  # Empty for full migration
                data_config=data_config,
            )
            result["steps"].append(build_result)

            if build_result.get("code") != 0:
                result["error"] = f"Script build failed: {build_result.get('message')}"
                result["end_time"] = time.time()
                return result

            # Get script names from response data
            script_data = build_result.get("data", {})
            script_names = script_data.get("scriptNames", []) if isinstance(script_data, dict) else script_data

            if not script_names:
                result["error"] = "No scripts generated"
                result["end_time"] = time.time()
                return result

            # Step 6: Execute migration
            exec_result = self.execute_migration_script(script_names)
            result["steps"].append(exec_result)

            if exec_result.get("code") != 0:
                result["error"] = f"Migration execution failed: {exec_result.get('message')}"
                result["end_time"] = time.time()
                return result

            # Step 7: Wait for completion
            final_status = self.wait_for_completion(
                script_names[0], timeout=timeout, poll_interval=poll_interval
            )
            result["steps"].append(final_status)
            result["final_status"] = final_status.get("final_status")
            result["success"] = final_status.get("final_status") == MigrationStatus.SUCCEEDED.value

        except Exception as e:
            logger.error(f"Workflow error: {e}")
            result["error"] = str(e)

        result["end_time"] = time.time()
        result["elapsed_time"] = result["end_time"] - result["start_time"]

        logger.info(f"Workflow completed: success={result['success']}, elapsed={result['elapsed_time']:.1f}s")
        return result

    def run_schema_only_migration(
        self,
        source_config: Dict[str, Any],
        target_config: Dict[str, Any],
        metadata_options: Optional[Dict[str, Any]] = None,
        execute_ddl_confirm: Optional[Callable[[Dict[str, Any]], bool]] = None,
    ) -> Dict[str, Any]:
        """
        Run schema-only migration workflow (DDL only, no data).

        Args:
            source_config: Source database configuration
            target_config: Target KAIWUDB configuration
            metadata_options: Metadata extraction options
            execute_ddl_confirm: Callback to confirm DDL execution

        Returns:
            Complete workflow result
        """
        workflow_id = f"WF_SCHEMA_{int(time.time())}"
        logger.info(f"Starting schema-only migration workflow: {workflow_id}")

        result = {
            "workflow_id": workflow_id,
            "workflow_type": MigrationWorkflow.SCHEMA_ONLY.value,
            "start_time": time.time(),
            "steps": [],
            "success": False,
        }

        try:
            # Step 1: Test connections
            conn_result = self.test_connections(source_config, target_config)
            result["steps"].append(conn_result)

            if not conn_result["all_ok"]:
                result["error"] = "Connection test failed"
                result["end_time"] = time.time()
                return result

            # Step 2: Read source metadata
            meta_result = self.read_source_metadata(source_config, metadata_options)
            result["steps"].append(meta_result)

            if meta_result.get("code") != 0:
                result["error"] = f"Metadata reading failed: {meta_result.get('message')}"
                result["end_time"] = time.time()
                return result

            source_db = meta_result.get("data", {})

            # Step 3: Preview DDL
            # Determine if time series based on source type (auto-detect engine)
            source_type = source_config.get("type", "")
            is_time_series = (
                source_config.get("engine") == "TIMESERIES" or
                DataSourceManager.get_engine(source_type) == "TIMESERIES"
            )
            ddl_preview = self.preview_ddl(
                target_config, source_db, metadata_options,
                is_time_series=is_time_series
            )
            result["steps"].append(ddl_preview)

            if ddl_preview.get("code") != 0:
                result["error"] = f"DDL preview failed: {ddl_preview.get('message')}"
                result["end_time"] = time.time()
                return result

            # Step 4: Execute DDL (with optional confirmation)
            if execute_ddl_confirm:
                if not execute_ddl_confirm(ddl_preview):
                    result["error"] = "DDL execution not confirmed by user"
                    result["end_time"] = time.time()
                    return result

            ddl_execute = self.execute_ddl(target_config, ddl_preview.get("data", {}))
            result["steps"].append(ddl_execute)

            result["success"] = ddl_execute.get("code") == 0

        except Exception as e:
            logger.error(f"Workflow error: {e}")
            result["error"] = str(e)

        result["end_time"] = time.time()
        result["elapsed_time"] = result["end_time"] - result["start_time"]

        return result

    def run_data_only_migration(
        self,
        source_config: Dict[str, Any],
        target_config: Dict[str, Any],
        tables: List[Dict[str, Any]],
        data_config: Optional[Dict[str, Any]] = None,
        timeout: int = 3600,
        poll_interval: int = 2,
    ) -> Dict[str, Any]:
        """
        Run data-only migration workflow (tables must exist).

        Args:
            source_config: Source database configuration
            target_config: Target KAIWUDB configuration
            tables: Table mappings (required for data-only)
            data_config: Data migration settings
            timeout: Overall timeout in seconds
            poll_interval: Status check interval

        Returns:
            Complete workflow result
        """
        workflow_id = f"WF_DATA_{int(time.time())}"
        logger.info(f"Starting data-only migration workflow: {workflow_id}")

        result = {
            "workflow_id": workflow_id,
            "workflow_type": MigrationWorkflow.DATA_ONLY.value,
            "start_time": time.time(),
            "steps": [],
            "success": False,
        }

        try:
            # Step 1: Test connections
            conn_result = self.test_connections(source_config, target_config)
            result["steps"].append(conn_result)

            if not conn_result["all_ok"]:
                result["error"] = "Connection test failed"
                result["end_time"] = time.time()
                return result

            # Step 2: Build migration script (tables required)
            build_result = self.build_migration_script(
                source_config, target_config,
                tables=tables,
                data_config=data_config,
            )
            result["steps"].append(build_result)

            if build_result.get("code") != 0:
                result["error"] = f"Script build failed: {build_result.get('message')}"
                result["end_time"] = time.time()
                return result

            # Get script names from response data
            script_data = build_result.get("data", {})
            script_names = script_data.get("scriptNames", []) if isinstance(script_data, dict) else script_data

            if not script_names:
                result["error"] = "No scripts generated"
                result["end_time"] = time.time()
                return result

            # Step 3: Execute migration
            exec_result = self.execute_migration_script(script_names)
            result["steps"].append(exec_result)

            if exec_result.get("code") != 0:
                result["error"] = f"Migration execution failed: {exec_result.get('message')}"
                result["end_time"] = time.time()
                return result

            # Step 4: Wait for completion
            final_status = self.wait_for_completion(
                script_names[0], timeout=timeout, poll_interval=poll_interval
            )
            result["steps"].append(final_status)
            result["final_status"] = final_status.get("final_status")
            result["success"] = final_status.get("final_status") == MigrationStatus.SUCCEEDED.value

        except Exception as e:
            logger.error(f"Workflow error: {e}")
            result["error"] = str(e)

        result["end_time"] = time.time()
        result["elapsed_time"] = result["end_time"] - result["start_time"]

        return result

    def run_table_level_migration(
        self,
        source_config: Dict[str, Any],
        target_config: Dict[str, Any],
        tables: List[Dict[str, Any]],
        data_config: Optional[Dict[str, Any]] = None,
        timeout: int = 3600,
        poll_interval: int = 2,
    ) -> Dict[str, Any]:
        """
        Run table-level migration workflow (for restricted sources).

        Args:
            source_config: Source database configuration
            target_config: Target KAIWUDB configuration
            tables: Table mappings
            data_config: Data migration settings
            timeout: Overall timeout in seconds
            poll_interval: Status check interval

        Returns:
            Complete workflow result
        """
        # Table-level is same as data-only from KDTS perspective
        result = self.run_data_only_migration(
            source_config, target_config, tables, data_config, timeout, poll_interval
        )
        result["workflow_type"] = MigrationWorkflow.TABLE_LEVEL.value
        return result

    # ==================== Workflow History ====================

    def get_workflow_history(self) -> List[Dict[str, Any]]:
        """
        Get history of all workflow steps.

        Returns:
            List of step results
        """
        return list(self._workflow_history)

    def clear_workflow_history(self):
        """Clear workflow history."""
        self._workflow_history.clear()

    def get_current_step(self) -> Optional[str]:
        """
        Get current workflow step.

        Returns:
            Current step name or None
        """
        return self._current_step.value if self._current_step else None

    # ==================== Batch Operations ====================

    def run_batch_migration(
        self,
        source_config: Dict[str, Any],
        target_config: Dict[str, Any],
        table_batches: List[List[Dict[str, Any]]],
        data_config: Optional[Dict[str, Any]] = None,
        timeout_per_batch: int = 1800,
        poll_interval: int = 2,
    ) -> Dict[str, Any]:
        """
        Run migration in batches (for large datasets).

        Args:
            source_config: Source database configuration
            target_config: Target KAIWUDB configuration
            table_batches: List of table mapping batches
            data_config: Data migration settings
            timeout_per_batch: Timeout for each batch
            poll_interval: Status check interval

        Returns:
            Batch migration result with per-batch status
        """
        workflow_id = f"WF_BATCH_{int(time.time())}"
        logger.info(f"Starting batch migration workflow: {workflow_id}")

        result = {
            "workflow_id": workflow_id,
            "workflow_type": "batch_migration",
            "start_time": time.time(),
            "total_batches": len(table_batches),
            "batch_results": [],
            "success": True,
        }

        for batch_idx, tables in enumerate(table_batches):
            logger.info(f"Processing batch {batch_idx + 1}/{len(table_batches)} ({len(tables)} tables)")

            batch_result = self.run_data_only_migration(
                source_config=source_config,
                target_config=target_config,
                tables=tables,
                data_config=data_config,
                timeout=timeout_per_batch,
                poll_interval=poll_interval,
            )

            batch_result["batch_index"] = batch_idx
            result["batch_results"].append(batch_result)

            if not batch_result["success"]:
                logger.error(f"Batch {batch_idx + 1} failed, stopping")
                result["success"] = False
                result["failed_batch"] = batch_idx
                break

        result["end_time"] = time.time()
        result["elapsed_time"] = result["end_time"] - result["start_time"]
        result["completed_batches"] = len([
            r for r in result["batch_results"] if r["success"]
        ])

        return result


# Convenience functions (module-level)

def create_workflow_manager(api_client) -> MigrationWorkflowManager:
    """
    Create a MigrationWorkflowManager instance.

    Args:
        api_client: KDTS API client

    Returns:
        Workflow manager instance
    """
    return MigrationWorkflowManager(api_client)


if __name__ == "__main__":
    # Demo - requires KDTS API client
    print("Migration Workflow Manager Demo")
    print("=" * 50)

    # Note: This is a dry-run demo without actual API calls
    manager = MigrationWorkflowManager()

    print("\nSupported workflows:")
    for wf in MigrationWorkflow:
        print(f"  - {wf.value}")

    print("\nSupported steps:")
    for step in MigrationStep:
        print(f"  - {step.value}")

    print("\nTask statuses:")
    for status in MigrationStatus:
        print(f"  - {status.value}")

    print("\nWorkflow manager ready. Initialize with api_client to use.")