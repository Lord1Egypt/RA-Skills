import zipfile
import os

def unzip_file(zip_path):
    extract_path = zip_path.replace("downloads", "extracted").replace(".zip", "")

    os.makedirs(extract_path, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    return extract_path