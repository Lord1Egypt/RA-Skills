"""
v2_l6_decrypt.py - L6 Encryption handling for pdf_text_replace v2.0
Uses pikepdf to decrypt owner-protected or password-protected PDFs.
"""

from pypdf import PdfReader


def is_encrypted(pdf_path: str) -> bool:
    """Return True if the PDF is encrypted."""
    try:
        r = PdfReader(str(pdf_path))
        return r.is_encrypted
    except Exception:
        return False


def decrypt_pdf(input_path: str, output_path: str, password: str = "") -> bool:
    """
    Decrypt an encrypted PDF and save the decrypted copy to output_path.
    Tries empty password first (handles owner-only PDFs), then the provided password.
    Falls back to pikepdf for more encryption variants.

    Returns True on success.
    """
    input_path = str(input_path)

    # Strategy 1: pypdf with empty password (owner-only PDFs)
    try:
        reader = PdfReader(input_path)
        if reader.is_encrypted:
            result = reader.decrypt("")
            if result > 0:
                from pypdf import PdfWriter
                writer = PdfWriter()
                writer.append_pages_from_reader(reader)
                with open(output_path, "wb") as f:
                    writer.write(f)
                print("[L6] Decrypted with pypdf (owner-only, empty password)")
                return True
    except Exception as e:
        print(f"[L6] pypdf empty-password attempt failed: {e}")

    # Strategy 2: pypdf with provided password
    if password:
        try:
            reader = PdfReader(input_path)
            result = reader.decrypt(password)
            if result > 0:
                from pypdf import PdfWriter
                writer = PdfWriter()
                writer.append_pages_from_reader(reader)
                with open(output_path, "wb") as f:
                    writer.write(f)
                print("[L6] Decrypted with pypdf + supplied password")
                return True
        except Exception as e:
            print(f"[L6] pypdf with password failed: {e}")

    # Strategy 3: pikepdf
    try:
        import pikepdf
        try:
            pdf = pikepdf.open(input_path, password=password or "")
            pdf.save(output_path)
            pdf.close()
            print("[L6] Decrypted with pikepdf")
            return True
        except pikepdf.PasswordError:
            print("[L6] pikepdf: wrong password")
        except Exception as e:
            print(f"[L6] pikepdf failed: {e}")
    except ImportError:
        print("[L6] pikepdf not available (pip install pikepdf)")

    return False
