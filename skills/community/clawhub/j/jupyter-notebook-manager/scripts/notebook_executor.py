#!/usr/bin/env python3
"""
Jupyter Notebook Executor
Execute notebooks with monitoring, error handling, and output capture.
"""

import json
import argparse
import subprocess
import time
from pathlib import Path
from typing import Dict, Optional, Any, List
from datetime import datetime
import sys


class NotebookExecutor:
    """Execute Jupyter notebooks with robust error handling."""
    
    def __init__(self, timeout: int = 600):
        """
        Initialize executor.
        
        Args:
            timeout: Maximum execution time in seconds (default: 10 min)
        """
        self.timeout = timeout
    
    def execute(
        self,
        notebook_path: str,
        output_path: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        kernel: str = "python3",
        verbose: bool = True,
    ) -> Dict[str, Any]:
        """
        Execute a Jupyter notebook.
        
        Args:
            notebook_path: Path to input notebook
            output_path: Path for executed notebook (default: overwrite input)
            parameters: Parameters to inject
            kernel: Kernel name
            verbose: Print progress
        
        Returns:
            Execution result dict with status, timing, errors
        """
        notebook_path = Path(notebook_path)
        if not notebook_path.exists():
            return {
                "status": "error",
                "error": f"Notebook not found: {notebook_path}",
                "execution_time": 0,
            }
        
        output_path = Path(output_path) if output_path else notebook_path
        
        if verbose:
            print(f"📓 Executing notebook: {notebook_path}")
            print(f"   Output: {output_path}")
            if parameters:
                print(f"   Parameters: {parameters}")
        
        start_time = time.time()
        
        try:
            # Load notebook
            with open(notebook_path, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
            
            # Inject parameters if provided
            if parameters:
                notebook = self._inject_parameters(notebook, parameters)
            
            # Execute using nbconvert
            result = self._execute_with_nbconvert(
                notebook,
                output_path,
                kernel,
                verbose
            )
            
            execution_time = time.time() - start_time
            
            if result["status"] == "success":
                if verbose:
                    print(f"✅ Execution completed in {execution_time:.2f}s")
                
                # Extract outputs
                outputs = self._extract_outputs(output_path)
                
                return {
                    "status": "success",
                    "execution_time": execution_time,
                    "output_path": str(output_path),
                    "cell_count": len(notebook.get("cells", [])),
                    "outputs": outputs,
                }
            else:
                if verbose:
                    print(f"❌ Execution failed after {execution_time:.2f}s")
                    print(f"   Error: {result.get('error', 'Unknown error')}")
                
                return {
                    "status": "error",
                    "execution_time": execution_time,
                    "error": result.get("error"),
                    "error_cell": result.get("error_cell"),
                }
        
        except Exception as e:
            execution_time = time.time() - start_time
            if verbose:
                print(f"❌ Exception during execution: {e}")
            
            return {
                "status": "error",
                "execution_time": execution_time,
                "error": str(e),
            }
    
    def _inject_parameters(
        self,
        notebook: Dict,
        parameters: Dict[str, Any]
    ) -> Dict:
        """Inject parameters into notebook as first code cell."""
        # Create parameter cell
        param_cell = {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {"tags": ["parameters"]},
            "outputs": [],
            "source": [
                "# Injected parameters\n"
            ]
        }
        
        for key, value in parameters.items():
            if isinstance(value, str):
                param_cell["source"].append(f"{key} = '{value}'\n")
            else:
                param_cell["source"].append(f"{key} = {value}\n")
        
        # Insert at beginning (after first markdown if present)
        cells = notebook.get("cells", [])
        insert_pos = 1 if cells and cells[0]["cell_type"] == "markdown" else 0
        cells.insert(insert_pos, param_cell)
        notebook["cells"] = cells
        
        return notebook
    
    def _execute_with_nbconvert(
        self,
        notebook: Dict,
        output_path: Path,
        kernel: str,
        verbose: bool
    ) -> Dict[str, Any]:
        """Execute notebook using nbconvert."""
        # Write temporary notebook
        temp_path = output_path.parent / f".tmp_{output_path.name}"
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=2)
        
        try:
            # Execute with jupyter nbconvert
            cmd = [
                "jupyter", "nbconvert",
                "--to", "notebook",
                "--execute",
                "--inplace",
                f"--ExecutePreprocessor.kernel_name={kernel}",
                f"--ExecutePreprocessor.timeout={self.timeout}",
                "--ExecutePreprocessor.allow_errors=True",
                str(temp_path),
            ]
            
            if verbose:
                print(f"🔧 Running: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout + 60  # Extra buffer
            )
            
            if result.returncode != 0:
                error_msg = result.stderr or result.stdout
                return {
                    "status": "error",
                    "error": f"nbconvert failed: {error_msg}"
                }
            
            # Move temp to output
            temp_path.replace(output_path)
            
            # Check for execution errors in notebook
            with open(output_path, 'r', encoding='utf-8') as f:
                executed_nb = json.load(f)
            
            error_info = self._check_for_errors(executed_nb)
            if error_info:
                return {
                    "status": "error",
                    **error_info
                }
            
            return {"status": "success"}
        
        except subprocess.TimeoutExpired:
            return {
                "status": "error",
                "error": f"Execution timeout ({self.timeout}s exceeded)"
            }
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
        
        finally:
            # Cleanup temp file
            if temp_path.exists():
                temp_path.unlink()
    
    def _check_for_errors(self, notebook: Dict) -> Optional[Dict]:
        """Check if any cell has errors."""
        for idx, cell in enumerate(notebook.get("cells", []), 1):
            if cell.get("cell_type") != "code":
                continue
            
            for output in cell.get("outputs", []):
                if output.get("output_type") == "error":
                    return {
                        "error": output.get("ename", "Unknown error"),
                        "error_message": "\n".join(output.get("traceback", [])),
                        "error_cell": idx,
                    }
        
        return None
    
    def _extract_outputs(self, notebook_path: Path) -> List[Dict]:
        """Extract key outputs from executed notebook."""
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        outputs = []
        
        for idx, cell in enumerate(notebook.get("cells", []), 1):
            if cell.get("cell_type") != "code":
                continue
            
            cell_outputs = []
            for output in cell.get("outputs", []):
                output_type = output.get("output_type")
                
                if output_type == "stream":
                    text = "".join(output.get("text", []))
                    if text.strip():
                        cell_outputs.append({
                            "type": "text",
                            "content": text[:500]  # Limit size
                        })
                
                elif output_type == "execute_result":
                    data = output.get("data", {})
                    if "text/plain" in data:
                        cell_outputs.append({
                            "type": "result",
                            "content": "".join(data["text/plain"])[:500]
                        })
                
                elif output_type == "display_data":
                    data = output.get("data", {})
                    if "image/png" in data:
                        cell_outputs.append({
                            "type": "image",
                            "content": "[PNG image]"
                        })
                    elif "text/plain" in data:
                        cell_outputs.append({
                            "type": "display",
                            "content": "".join(data["text/plain"])[:500]
                        })
            
            if cell_outputs:
                outputs.append({
                    "cell": idx,
                    "outputs": cell_outputs
                })
        
        return outputs


def main():
    """CLI interface."""
    parser = argparse.ArgumentParser(description="Execute Jupyter notebooks")
    parser.add_argument("notebook", help="Notebook path")
    parser.add_argument("--output", help="Output path (default: overwrite input)")
    parser.add_argument("--timeout", type=int, default=600, help="Timeout in seconds")
    parser.add_argument("--kernel", default="python3", help="Kernel name")
    parser.add_argument("--param", action="append", help="Parameters (key=value)")
    parser.add_argument("--quiet", action="store_true", help="Suppress output")
    
    args = parser.parse_args()
    
    # Parse parameters
    parameters = {}
    if args.param:
        for param in args.param:
            key, value = param.split("=", 1)
            # Try to parse as number
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    pass  # Keep as string
            parameters[key] = value
    
    executor = NotebookExecutor(timeout=args.timeout)
    result = executor.execute(
        notebook_path=args.notebook,
        output_path=args.output,
        parameters=parameters if parameters else None,
        kernel=args.kernel,
        verbose=not args.quiet,
    )
    
    # Exit with appropriate code
    sys.exit(0 if result["status"] == "success" else 1)


if __name__ == "__main__":
    main()
