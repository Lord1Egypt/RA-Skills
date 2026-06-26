#!/usr/bin/env python3
"""
Mermaid Image Generation and Image Host Uploader
Designed for WeChat Official Account articles
"""
import os
import re
import argparse
from typing import List, Tuple, Optional
from mermaid_converter import MermaidConverter
from image_host_uploader import ImageHostUploader


class MermaidUploader:
    """Mermaid Uploader"""

    def __init__(self):
        self.converter = MermaidConverter()
        self.uploader = ImageHostUploader()

    def convert_and_upload(
        self,
        mermaid_code: str,
        image_host: str = 'freeimage',
        output_format: str = 'png',
        **kwargs
    ) -> Optional[str]:
        """
        Convert Mermaid and upload to image host

        Args:
            mermaid_code: Mermaid code
            image_host: Image host name
            output_format: Output format
            **kwargs: Other parameters

        Returns:
            Image URL or None
        """
        print("=" * 60)
        print("Mermaid Image Generation and Upload")
        print("=" * 60)

        # 1. Convert Mermaid
        print("\n[1/3] Converting Mermaid diagram...")
        image_path = self.converter.convert(
            mermaid_code,
            output_format=output_format
        )

        if not image_path:
            print("Conversion failed")
            return None

        print(f"Converted successfully: {image_path}")

        # If HTML format, don't upload
        if output_format == 'html':
            print("\nHTML format doesn't need upload")
            print(f"Please open in browser: {image_path}")
            return None

        # 2. Upload to image host
        print(f"\n[2/3] Uploading to {image_host}...")
        url = self.uploader.upload(image_path, image_host, **kwargs)

        if not url:
            print("Upload failed")
            print(f"Image saved to: {image_path}")
            return None

        print(f"Uploaded successfully: {url}")

        # 3. Complete
        print("\n[3/3] Complete!")
        print(f"\nMarkdown image code:")
        print(f"![Mermaid Diagram]({url})")

        return url


class MarkdownProcessor:
    """Markdown Processor - Batch replace Mermaid diagrams"""

    def __init__(self):
        self.uploader = MermaidUploader()
        self.mermaid_pattern = re.compile(
            r'```mermaid\s*([\s\S]*?)\s*```',
            re.MULTILINE
        )

    def extract_mermaid_blocks(self, markdown_text: str) -> List[Tuple[int, int, str]]:
        """
        Extract all Mermaid code blocks from Markdown

        Returns:
            List of (start, end, code)
        """
        blocks = []
        for match in self.mermaid_pattern.finditer(markdown_text):
            blocks.append((match.start(), match.end(), match.group(1).strip()))
        return blocks

    def process_file(
        self,
        input_path: str,
        output_path: str,
        image_host: str = 'freeimage'
    ) -> str:
        """
        Process Markdown file, replace Mermaid with images

        Args:
            input_path: Input file path
            output_path: Output file path
            image_host: Image host name

        Returns:
            Processed text
        """
        print("=" * 60)
        print("Markdown File Processing")
        print("=" * 60)

        # Read file
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract Mermaid blocks
        blocks = self.extract_mermaid_blocks(content)
        print(f"\nFound {len(blocks)} Mermaid diagrams")

        if blocks:
            # Replace from back to front (avoid position shift)
            for i, (start, end, code) in reversed(list(enumerate(blocks))):
                print(f"\nProcessing diagram {len(blocks)-i}/{len(blocks)}...")

                # Convert and upload
                url = self.uploader.convert_and_upload(
                    code,
                    image_host=image_host
                )

                if url:
                    # Replace with image
                    markdown_image = f"![Diagram {i+1}]({url})"
                    content = content[:start] + markdown_image + content[end:]
                    print(f"Replaced: {markdown_image}")
                else:
                    print(f"Skipped diagram {i+1}")

        # Save result
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"\nProcessing complete: {output_path}")
        return content


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Mermaid Image Generation and Upload Tool'
    )

    parser.add_argument(
        '--input', '-i',
        help='Input Mermaid file'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output image file'
    )
    parser.add_argument(
        '--markdown', '-m',
        help='Markdown file to process'
    )
    parser.add_argument(
        '--output-markdown',
        help='Output Markdown file'
    )
    parser.add_argument(
        '--upload', '-u',
        action='store_true',
        help='Upload to image host'
    )
    parser.add_argument(
        '--image-host',
        default='freeimage',
        help='Image host (freeimage, postimages, imgur)'
    )
    parser.add_argument(
        '--format', '-f',
        default='png',
        help='Output format (png, svg, jpg, html)'
    )
    parser.add_argument(
        '--api-key',
        help='Image host API Key'
    )
    parser.add_argument(
        '--code', '-c',
        help='Direct Mermaid code input'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run test'
    )

    args = parser.parse_args()

    # Test mode
    if args.test:
        print("Running test...")
        test_code = """
graph LR
    A[Start] --> B[Process]
    B --> C[End]
"""
        uploader = MermaidUploader()
        url = uploader.convert_and_upload(
            test_code,
            output_format='html'
        )
        return

    # Process Markdown file
    if args.markdown:
        processor = MarkdownProcessor()
        output_md = args.output_markdown or args.markdown.replace('.md', '_with_images.md')
        processor.process_file(
            args.markdown,
            output_md,
            image_host=args.image_host
        )
        return

    # Read Mermaid code from file
    mermaid_code = ""

    if args.code:
        mermaid_code = args.code
    elif args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            mermaid_code = f.read()
    else:
        print("Please use --code or --input to specify Mermaid content")
        print("Or use --markdown to process a Markdown file")
        print("Use --help for more info")
        return

    # Convert
    uploader = MermaidUploader()

    if args.upload:
        url = uploader.convert_and_upload(
            mermaid_code,
            image_host=args.image_host,
            output_format=args.format,
            api_key=args.api_key
        )
        if url:
            print(f"\nSuccess: {url}")
    else:
        # Convert only, no upload
        image_path = uploader.converter.convert(
            mermaid_code,
            args.output,
            args.format
        )
        if image_path:
            print(f"Converted successfully: {image_path}")


if __name__ == '__main__':
    main()
