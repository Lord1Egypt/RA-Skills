#!/usr/bin/env python3
"""
Batch JSON Processor - Verarbeitet mehrere JSON-Dateien oder JSON-Lines (NDJSON).
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Iterator, Optional, Callable, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback

try:
    from pydantic import BaseModel
    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False

from json_processor import parse_json, parse_and_validate, JSONProcessingError


class BatchResult:
    """Ergebnis einer Batch-Verarbeitung."""
    
    def __init__(self, index: int, source: str, success: bool, 
                 data: Any = None, error: Optional[str] = None):
        self.index = index
        self.source = source
        self.success = success
        self.data = data
        self.error = error
    
    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "source": self.source,
            "success": self.success,
            "data": self.data,
            "error": self.error
        }


def read_jsonl(file_path: Path) -> Iterator[dict]:
    """
    Liest JSON-Lines (NDJSON) Datei Zeile für Zeile.
    
    Args:
        file_path: Pfad zur .jsonl oder .ndjson Datei
    
    Yields:
        Geparste JSON-Objekte
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as e:
                yield BatchResult(
                    index=line_num,
                    source=f"{file_path}:{line_num}",
                    success=False,
                    error=f"JSON decode error: {e}"
                )


def process_batch(
    inputs: list,
    processor: Callable[[str, int], BatchResult],
    max_workers: int = 4
) -> list[BatchResult]:
    """
    Verarbeitet eine Liste von Inputs parallel.
    
    Args:
        inputs: Liste der zu verarbeitenden Eingaben (Strings oder Pfade)
        processor: Funktion, die (input, index) -> BatchResult zurückgibt
        max_workers: Anzahl paralleler Worker
    
    Returns:
        Liste der BatchResult-Objekte
    """
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(processor, inp, idx): idx 
            for idx, inp in enumerate(inputs)
        }
        
        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                idx = futures[future]
                results.append(BatchResult(
                    index=idx,
                    source=str(inputs[idx]),
                    success=False,
                    error=f"Unexpected error: {str(e)}"
                ))
    
    # Sortiere nach Index
    results.sort(key=lambda x: x.index)
    return results


def process_file_batch(
    file_paths: list[Path],
    repair: bool = True,
    validate_model: Optional[type] = None,
    max_workers: int = 4
) -> list[BatchResult]:
    """
    Verarbeitet mehrere JSON-Dateien im Batch.
    
    Args:
        file_paths: Liste der Datei-Pfade
        repair: Ob JSON-Reparatur angewendet werden soll
        validate_model: Optionales Pydantic-Modell für Validierung
        max_workers: Parallele Worker
    
    Returns:
        Liste der BatchResult-Objekte
    """
    def processor(path: Path, idx: int) -> BatchResult:
        try:
            content = Path(path).read_text(encoding='utf-8')
            
            if validate_model and HAS_PYDANTIC:
                data = parse_and_validate(content, validate_model, repair=repair)
            else:
                data = parse_json(content, repair=repair)
            
            return BatchResult(
                index=idx,
                source=str(path),
                success=True,
                data=data
            )
        except JSONProcessingError as e:
            return BatchResult(
                index=idx,
                source=str(path),
                success=False,
                error=str(e)
            )
        except Exception as e:
            return BatchResult(
                index=idx,
                source=str(path),
                success=False,
                error=f"{type(e).__name__}: {str(e)}"
            )
    
    return process_batch(file_paths, processor, max_workers)


def process_jsonl_file(
    file_path: Path,
    repair: bool = True,
    validate_model: Optional[type] = None
) -> list[BatchResult]:
    """
    Verarbeitet eine JSON-Lines Datei.
    
    Args:
        file_path: Pfad zur .jsonl Datei
        repair: Ob Reparatur angewendet werden soll
        validate_model: Optionales Pydantic-Modell
    
    Returns:
        Liste der BatchResult-Objekte
    """
    results = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            try:
                if validate_model and HAS_PYDANTIC:
                    data = parse_and_validate(line, validate_model, repair=repair)
                else:
                    data = parse_json(line, repair=repair)
                
                results.append(BatchResult(
                    index=line_num,
                    source=f"{file_path}:{line_num}",
                    success=True,
                    data=data
                ))
            except JSONProcessingError as e:
                results.append(BatchResult(
                    index=line_num,
                    source=f"{file_path}:{line_num}",
                    success=False,
                    error=str(e)
                ))
    
    return results


def write_jsonl(results: list[BatchResult], output_path: Path, only_successful: bool = True):
    """
    Schreibt BatchResult-Liste als JSON-Lines.
    
    Args:
        results: Liste der Ergebnisse
        output_path: Ausgabedatei
        only_successful: Nur erfolgreiche Ergebnisse schreiben
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        for result in results:
            if only_successful and not result.success:
                continue
            f.write(json.dumps(result.to_dict(), ensure_ascii=False) + '\n')


def main():
    parser = argparse.ArgumentParser(description="Batch JSON Processor")
    parser.add_argument("inputs", nargs='+', help="JSON files to process")
    parser.add_argument("--jsonl", "-l", action="store_true", help="Treat inputs as JSON-Lines files")
    parser.add_argument("--repair", "-r", action="store_true", default=True, help="Enable JSON repair")
    parser.add_argument("--workers", "-w", type=int, default=4, help="Parallel workers")
    parser.add_argument("--output", "-o", help="Output JSON-Lines file")
    parser.add_argument("--summary", "-s", action="store_true", help="Show summary only")
    
    args = parser.parse_args()
    
    all_results = []
    
    if args.jsonl:
        # JSON-Lines Modus
        for input_path in args.inputs:
            results = process_jsonl_file(Path(input_path), repair=args.repair)
            all_results.extend(results)
    else:
        # Standard JSON Batch
        file_paths = [Path(p) for p in args.inputs]
        all_results = process_file_batch(
            file_paths, 
            repair=args.repair, 
            max_workers=args.workers
        )
    
    # Ausgabe
    successful = sum(1 for r in all_results if r.success)
    failed = len(all_results) - successful
    
    if args.summary:
        print(f"Processed: {len(all_results)}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
    else:
        for result in all_results:
            if result.success:
                print(json.dumps(result.data, ensure_ascii=False))
            else:
                print(f"ERROR [{result.source}]: {result.error}", file=sys.stderr)
    
    # Optional: JSONL Output
    if args.output:
        write_jsonl(all_results, Path(args.output), only_successful=False)
        print(f"\nResults written to: {args.output}", file=sys.stderr)
    
    # Exit code
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
