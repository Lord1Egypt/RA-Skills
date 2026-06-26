"""
Mermaid Diagram Converter
Support multiple conversion methods
"""
import os
import subprocess
import tempfile
from typing import Optional


class MermaidConverter:
    """Mermaid Converter"""

    def __init__(self):
        self.temp_dir = tempfile.gettempdir()

    def check_mermaid_cli(self) -> bool:
        """Check if mermaid-cli is installed"""
        try:
            result = subprocess.run(
                ['mmdc', '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def convert_with_mermaid_cli(
        self,
        mermaid_code: str,
        output_path: str,
        output_format: str = 'png'
    ) -> bool:
        """
        Convert using mermaid-cli

        Args:
            mermaid_code: Mermaid code
            output_path: Output file path
            output_format: Output format (png, svg, jpg)

        Returns:
            Success or not
        """
        try:
            # Create temporary .mmd file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False, encoding='utf-8') as f:
                f.write(mermaid_code)
                temp_mmd = f.name

            try:
                # Build command
                cmd = [
                    'mmdc',
                    '-i', temp_mmd,
                    '-o', output_path,
                    '-f', output_format
                ]

                # Execute conversion
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

                if result.returncode == 0:
                    print(f"Converted successfully: {output_path}")
                    return True
                else:
                    print(f"Conversion failed: {result.stderr}")
                    return False

            finally:
                # Clean up temporary file
                if os.path.exists(temp_mmd):
                    os.unlink(temp_mmd)

        except Exception as e:
            print(f"Failed to convert with mermaid-cli: {e}")
            return False

    def convert_with_kroki(
        self,
        mermaid_code: str,
        output_path: str,
        output_format: str = 'png'
    ) -> bool:
        """
        Convert using Kroki online service

        Args:
            mermaid_code: Mermaid code
            output_path: Output file path
            output_format: Output format (png, svg, jpg)

        Returns:
            Success or not
        """
        try:
            import requests
            import base64
            import zlib

            # Compress and encode Mermaid code
            compressed = zlib.compress(mermaid_code.encode('utf-8'), 9)
            encoded = base64.urlsafe_b64encode(compressed).decode('utf-8')

            # Build URL
            url = f"https://kroki.io/mermaid/{output_format}/{encoded}"

            # Request
            response = requests.get(url, timeout=30)

            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                print(f"Converted successfully (Kroki): {output_path}")
                return True
            else:
                print(f"Kroki conversion failed: {response.status_code}")
                return False

        except ImportError:
            print("Please install requests: pip install requests")
            return False
        except Exception as e:
            print(f"Failed to convert with Kroki: {e}")
            return False

    def convert_with_mermaid_live(
        self,
        mermaid_code: str,
        output_path: str
    ) -> bool:
        """
        Simple alternative using Mermaid Live Editor
        Generate an HTML file that can be opened in browser and screenshotted

        Args:
            mermaid_code: Mermaid code
            output_path: Output HTML file path

        Returns:
            Success or not
        """
        try:
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Mermaid Diagram</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{ color: #333; }}
        .mermaid {{
            text-align: center;
            margin: 20px 0;
        }}
        .instructions {{
            background: #e7f3ff;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Diagram Preview</h1>

        <div class="instructions">
            <strong>Instructions:</strong>
            <ol>
                <li>Wait for diagram to render</li>
                <li>Right-click diagram -> "Save image as..."</li>
                <li>Or use screenshot tool</li>
            </ol>
        </div>

        <div class="mermaid">
{mermaid_code}
        </div>
    </div>

    <script>
        mermaid.initialize({{ startOnLoad: true }});
    </script>
</body>
</html>
"""

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            print(f"Generated HTML file: {output_path}")
            print("Please open in browser and save as image")
            return True

        except Exception as e:
            print(f"Failed to generate HTML: {e}")
            return False

    def convert(
        self,
        mermaid_code: str,
        output_path: Optional[str] = None,
        output_format: str = 'png',
        method: Optional[str] = None
    ) -> Optional[str]:
        """
        Convert Mermaid code to image

        Args:
            mermaid_code: Mermaid code
            output_path: Output file path (optional)
            output_format: Output format (png, svg, jpg, html)
            method: Conversion method (cli, kroki, html)

        Returns:
            Output file path or None
        """
        # Generate output path if not specified
        if output_path is None:
            output_path = os.path.join(
                self.temp_dir,
                f"mermaid_diagram.{output_format}"
            )

        # HTML format
        if output_format == 'html':
            if self.convert_with_mermaid_live(mermaid_code, output_path):
                return output_path
            return None

        # Try specified method
        if method == 'cli' and self.check_mermaid_cli():
            if self.convert_with_mermaid_cli(mermaid_code, output_path, output_format):
                return output_path

        elif method == 'kroki':
            if self.convert_with_kroki(mermaid_code, output_path, output_format):
                return output_path

        elif method == 'html':
            html_path = output_path.replace(f'.{output_format}', '.html')
            if self.convert_with_mermaid_live(mermaid_code, html_path):
                return html_path

        # Auto select method
        else:
            # Try Kroki first
            print("Trying Kroki online conversion...")
            if self.convert_with_kroki(mermaid_code, output_path, output_format):
                return output_path

            # Try mermaid-cli
            if self.check_mermaid_cli():
                print("Trying mermaid-cli...")
                if self.convert_with_mermaid_cli(mermaid_code, output_path, output_format):
                    return output_path

            # Fallback to HTML
            print("Using HTML method...")
            html_path = output_path.replace(f'.{output_format}', '.html')
            if self.convert_with_mermaid_live(mermaid_code, html_path):
                return html_path

        return None


# Simple test
if __name__ == '__main__':
    converter = MermaidConverter()
    print("Mermaid Converter loaded successfully")

    test_code = """
graph LR
    A[Start] --> B{Check}
    B -->|Yes| C[Process]
    B -->|No| D[Skip]
    C --> E[End]
    D --> E
    """

    print("\nTesting conversion...")
    result = converter.convert(test_code, output_format='html')
    if result:
        print(f"Output file: {result}")
