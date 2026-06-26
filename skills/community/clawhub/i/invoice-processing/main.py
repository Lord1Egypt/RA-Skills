import sys
import glob
import os
import hashlib
import argparse
import re

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF is required. Please install it using 'pip install PyMuPDF'")
    sys.exit(1)

def get_file_md5(file_path):
    """Compute the MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def is_pdf_file(file_path):
    """Check if a file is a PDF by reading its signature."""
    try:
        with open(file_path, "rb") as f:
            header = f.read(5)
            return header == b"%PDF-"
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return False

def fix_pdf_extensions(directory):
    """Find files ending with '?' or '？', check if they are PDFs, and append '.pdf' (replacing the question mark)."""
    print("--- Step 0: Fixing PDF extensions for files ending with '?' or '？' ---")
    fixed_count = 0
    
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith('?') or filename.endswith('？'):
                file_path = os.path.join(root, filename)
                if is_pdf_file(file_path):
                    # Replace the '?' or '？' at the end with '.pdf'
                    new_file_path = file_path[:-1] + '.pdf'
                    print(f"Renaming: {file_path} -> {new_file_path}")
                    os.rename(file_path, new_file_path)
                    fixed_count += 1
                    
    print(f"Total extensions fixed: {fixed_count}\n")

def process_duplicates(directory):
    """Find and remove duplicate files based on MD5 hash."""
    print("--- Step 1: Checking for duplicate files ---")
    seen_hashes = {}
    duplicates_removed = 0
    
    for root, _, files in os.walk(directory):
        for filename in files:
            # Skip hidden files like .DS_Store
            if filename.startswith('.'):
                continue
                
            file_path = os.path.join(root, filename)
            file_hash = get_file_md5(file_path)
            
            if not file_hash:
                continue

            if file_hash in seen_hashes:
                print(f"Duplicate found and removed: {file_path} (same as {seen_hashes[file_hash]})")
                os.remove(file_path)
                duplicates_removed += 1
            else:
                seen_hashes[file_hash] = file_path
                
    print(f"Total duplicate files removed: {duplicates_removed}\n")

def remove_by_filename(directory, name_keyword="行程单"):
    """Remove files containing a specific keyword in their name."""
    print(f"--- Step 2: Removing files with '{name_keyword}' in filename ---")
    removed_count = 0
    
    for root, _, files in os.walk(directory):
        for filename in files:
            if name_keyword in filename:
                file_path = os.path.join(root, filename)
                print(f"Removing file: {file_path}")
                os.remove(file_path)
                removed_count += 1
                
    print(f"Total files removed: {removed_count}\n")

def check_pdf_content(directory, content_keyword):
    """Check if PDF files contain any of the target keywords (semicolon-separated)."""
    # Parse the keywords, splitting by ';' and ignoring empty strings
    keywords = [k.strip() for k in content_keyword.split(';') if k.strip()]
    if not keywords:
        print("--- Step 3: Skipped PDF content check (no valid keywords provided) ---")
        return

    keywords_display = ', '.join(f"'{k}'" for k in keywords)
    print(f"--- Step 3: Checking PDF content for missing keywords ({keywords_display}) ---")
    
    import shutil
    # Create the target output directories
    invoices_dir = os.path.join(directory, "invoices")
    unknown_dir = os.path.join(invoices_dir, "unknown")
    os.makedirs(unknown_dir, exist_ok=True)

    count_without_keyword = 0
    count_matched = 0
    
    pdf_files = glob.glob(os.path.join(directory, '**', '*.pdf'), recursive=True)
    
    for file_path in pdf_files:
        # Skip processing files that are already inside the invoices directory to avoid cyclic processing
        if file_path.startswith(invoices_dir + os.sep) or file_path == invoices_dir:
            continue

        try:
            doc = fitz.open(file_path)
            found = False
            for page in doc:
                text = page.get_text()
                if any(k in text for k in keywords):
                    found = True
                    break
            
            doc.close()

            if found:
                # Move to matched directory
                dest_path = os.path.join(invoices_dir, os.path.basename(file_path))
                shutil.move(file_path, dest_path)
                print(f"File matched keyword, moved to: {dest_path}")
                count_matched += 1
            else:
                # Move to unknown directory
                dest_path = os.path.join(unknown_dir, os.path.basename(file_path))
                print(f"File missing keywords ({keywords_display}), moved to: {dest_path}")
                shutil.move(file_path, dest_path)
                count_without_keyword += 1
                
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    print(f"Total PDF files matched: {count_matched}")
    print(f"Total PDF files missing the keywords: {count_without_keyword}\n")

def calculate_total_amount(directory):
    """Calculate the total amount from all valid invoice PDFs."""
    print("--- Step 4: Calculating total amount ---")
    total = 0.0
    
    for root, _, files in os.walk(directory):
        for filename in files:
            if not filename.lower().endswith('.pdf'):
                continue
                
            file_path = os.path.join(root, filename)
            amount = None
            
            # Method 1: Try parsing from filename (e.g. 260116_33.80_苏州.pdf)
            match = re.match(r'^\d{6}_([0-9.]+)_', filename)
            if match:
                try:
                    amount = float(match.group(1))
                except Exception:
                    pass
            
            # Method 2: Try parsing from PDF content (e.g. dzfp_... files)
            if amount is None:
                try:
                    doc = fitz.open(file_path)
                    text = ""
                    for page in doc:
                        text += page.get_text()
                    doc.close()
                    
                    text_clean = text.replace(' ', '').replace('\n', '')
                    m = re.search(r'(?:小写|价税合计|总计)[^\d]*?[¥￥]?([0-9]+\.[0-9]{2})', text_clean)
                    if m:
                        amount = float(m.group(1))
                except Exception as e:
                    pass
            
            if amount is not None:
                total += amount
            else:
                print(f"Warning: Could not determine amount for {filename}")
                
    print(f"Grand Total Amount: {total:.2f} 元\n")
    return total

def main():
    parser = argparse.ArgumentParser(description="Process invoice PDF files.")
    parser.add_argument("command", choices=["process"], help="Command to run")
    parser.add_argument("keyword", help="Keyword(s) to check in PDF content (e.g., 银河科技;腾讯)")
    parser.add_argument("-d", "--dir", default=".", help="Target directory (default: current directory)")
    
    args = parser.parse_args()
    
    target_directory = os.path.abspath(args.dir)
    print(f"Processing directory: {target_directory}\n")
    
    if args.command == "process":
        fix_pdf_extensions(target_directory)
        process_duplicates(target_directory)
        remove_by_filename(target_directory, "行程单")
        check_pdf_content(target_directory, args.keyword)
        calculate_total_amount(target_directory)

if __name__ == "__main__":
    main()
