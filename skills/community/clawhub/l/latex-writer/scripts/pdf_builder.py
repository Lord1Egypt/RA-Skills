#!/usr/bin/env python3
"""
PDF Builder - Compile LaTeX to PDF
"""

import asyncio
import tempfile
import shutil
from pathlib import Path
from typing import Optional, Tuple
from dataclasses import dataclass


@dataclass
class BuildResult:
    """PDF build result"""
    success: bool
    pdf_path: Optional[Path] = None
    pdf_bytes: Optional[bytes] = None
    error_message: str = ""
    warnings: list = None
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []


class PDFBuilder:
    """Build PDF from LaTeX source"""
    
    DEFAULT_COMPILER = "xelatex"
    MAX_RUNS = 3
    
    def __init__(self, compiler: str = None, timeout: int = 120):
        self.compiler = compiler or self.DEFAULT_COMPILER
        self.timeout = timeout
        self._check_compiler()
    
    def _check_compiler(self):
        """Check if compiler is available"""
        if not shutil.which(self.compiler):
            raise RuntimeError(
                f"LaTeX compiler '{self.compiler}' not found. "
                "Please install TeX Live or MiKTeX."
            )
    
    async def build(
        self,
        latex_content: str,
        output_name: str = "document",
        work_dir: Optional[Path] = None
    ) -> BuildResult:
        """Build PDF from LaTeX content"""
        if work_dir is None:
            work_dir = Path(tempfile.mkdtemp(prefix="latex_build_"))
            cleanup = True
        else:
            work_dir = Path(work_dir)
            work_dir.mkdir(parents=True, exist_ok=True)
            cleanup = False
        
        try:
            tex_file = work_dir / f"{output_name}.tex"
            tex_file.write_text(latex_content, encoding='utf-8')
            
            result = await self._compile(tex_file, work_dir)
            
            if result.success:
                pdf_file = work_dir / f"{output_name}.pdf"
                if pdf_file.exists():
                    result.pdf_bytes = pdf_file.read_bytes()
                    result.pdf_path = pdf_file
                else:
                    result.success = False
                    result.error_message = "PDF file not generated"
            
            return result
        
        finally:
            if cleanup and work_dir.exists():
                shutil.rmtree(work_dir, ignore_errors=True)
    
    async def _compile(self, tex_file: Path, work_dir: Path) -> BuildResult:
        """Run LaTeX compilation with multiple passes"""
        result = BuildResult(success=True)
        
        for run in range(1, self.MAX_RUNS + 1):
            try:
                process = await asyncio.create_subprocess_exec(
                    self.compiler,
                    "-interaction=nonstopmode",
                    "-file-line-error",
                    "-halt-on-error",
                    str(tex_file),
                    cwd=work_dir,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                try:
                    stdout, stderr = await asyncio.wait_for(
                        process.communicate(),
                        timeout=self.timeout
                    )
                except asyncio.TimeoutError:
                    process.kill()
                    await process.wait()
                    result.success = False
                    result.error_message = f"Compilation timeout (>{self.timeout}s)"
                    return result
                
                stdout_text = stdout.decode('utf-8', errors='replace')
                stderr_text = stderr.decode('utf-8', errors='replace')
                
                if process.returncode != 0:
                    error_msg = self._parse_error(stdout_text, stderr_text)
                    result.success = False
                    result.error_message = error_msg
                    return result
                
                warnings = self._parse_warnings(stdout_text)
                result.warnings.extend(warnings)
                
                if run < self.MAX_RUNS and self._needs_rerun(stdout_text):
                    continue
                else:
                    break
            
            except Exception as e:
                result.success = False
                result.error_message = f"Compilation error: {str(e)}"
                return result
        
        return result
    
    def _parse_error(self, stdout: str, stderr: str) -> str:
        """Parse LaTeX error message"""
        lines = (stdout + "\n" + stderr).split("\n")
        
        for i, line in enumerate(lines):
            if "!" in line or "Error" in line or "error:" in line:
                context_start = max(0, i - 2)
                context_end = min(len(lines), i + 3)
                return "\n".join(lines[context_start:context_end])
        
        return stderr[:500] if stderr else "Unknown compilation error"
    
    def _parse_warnings(self, stdout: str) -> list:
        """Parse LaTeX warnings"""
        warnings = []
        lines = stdout.split("\n")
        
        for line in lines:
            if "Warning" in line or "warning:" in line:
                warning = line.strip()
                if len(warning) > 200:
                    warning = warning[:200] + "..."
                warnings.append(warning)
        
        return warnings[:10]
    
    def _needs_rerun(self, stdout: str) -> bool:
        """Check if another compilation run is needed"""
        indicators = [
            "Rerun",
            "rerun",
            "Label(s) may have changed",
            "Cross-references",
            "Citation(s) may have changed",
        ]
        
        return any(indicator in stdout for indicator in indicators)


if __name__ == "__main__":
    # Test code
    import asyncio
    
    async def test():
        # Simple test LaTeX
        latex = r"""
\documentclass{article}
\usepackage[utf8]{inputenc}
\begin{document}
Hello, World!
\end{document}
"""
        
        builder = PDFBuilder()
        result = await builder.build(latex, "test")
        
        if result.success:
            print("✓ PDF generated successfully!")
            print(f"  Size: {len(result.pdf_bytes)} bytes")
            
            # Save to file
            with open("/tmp/test.pdf", "wb") as f:
                f.write(result.pdf_bytes)
            print("  Saved to: /tmp/test.pdf")
        else:
            print(f"✗ Build failed:")
            print(result.error_message)
    
    asyncio.run(test())