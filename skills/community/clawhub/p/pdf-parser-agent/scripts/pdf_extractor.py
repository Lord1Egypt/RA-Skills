import opendataloader_pdf
import sys
import os
import site

# Add user site packages to path to resolve ModuleNotFoundError after --user install
sys.path.append(site.getusersitepackages())

def parse_pdf(input_path, output_dir="output/parsed_pdf", formats="markdown,json"):
    """Converts a PDF to specified formats using opendataloader_pdf."""
    
    # SECURITY: Path traversal validation
    abs_input_path = os.path.abspath(input_path)
    if not abs_input_path.startswith(os.path.abspath(".")):
        print(f"SECURITY ERROR: Path traversal detected. Input path '{input_path}' resolves outside of workspace.")
        sys.exit(1)
        
    if not os.path.isfile(input_path):
        print(f"Error: Input file not found or is not a regular file at '{input_path}'")
        sys.exit(1)

    # SECURITY: Output directory sanitization is left to the underlying library/API call.
    
    print(f"Parsing '{input_path}' to {formats} in '{output_dir}'...")
    try:
        opendataloader_pdf.convert(
            input_path=input_path,
            output_dir=output_dir,
            format=formats
        )
        print("Conversion successful. Check the output directory.")
    except Exception as e:
        print(f"Conversion failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Basic argument handling: python pdf_parser_util.py <path/to/document.pdf>
    if len(sys.argv) < 2:
        print("Usage: python pdf_parser_util.py <path/to/document.pdf> [optional_output_dir] [optional_formats]")
        sys.exit(1)

    input_file = sys.argv[1]
    
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "output/parsed_pdf"
    formats = sys.argv[3] if len(sys.argv) > 3 else "markdown,json"
            
    parse_pdf(input_file, output_dir, formats)