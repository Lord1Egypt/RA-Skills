
import argparse
import requests
import os

def upload_document(file_path, host, api_key, title=None, tags=None, document_type=None):
    """
    Uploads a document to Paperless-ngx and optionally assigns tags and a document type.
    """
    url = f"{host}/api/documents/"
    headers = {
        "Authorization": f"Token {api_key}"
    }

    files = {
        "document": (os.path.basename(file_path), open(file_path, "rb"), "application/octet-stream")
    }

    data = {}
    if title:
        data["title"] = title
    if tags:
        # Assuming tags should be sent as a list of strings
        # Paperless-ngx might expect tag IDs rather than names, this is a common variance.
        # This implementation assumes names and Paperless will create them if they don't exist
        # or associate by name if it does.
        data["tags"] = [tag.strip() for tag in tags.split(',')]
    if document_type:
        # Similar to tags, assuming document_type name. Paperless-ngx might expect document_type ID.
        # This will likely require looking up the document type ID first if the API doesn't support
        # setting by name directly during upload.
        data["document_type"] = document_type

    try:
        response = requests.post(url, headers=headers, files=files, data=data, verify=False) # verify=False for self-signed certs
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        print("Document uploaded successfully!")
        print(response.json())
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print(f"Http Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Ooops: Something Else: {err}")
    finally:
        # Ensure the file is closed after the request is complete
        files['document'][1].close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload and categorize documents to Paperless-ngx.")
    parser.add_argument("--file_path", required=True, help="Path to the document file to upload.")
    parser.add_argument("--host", required=True, help="Your Paperless-ngx host URL (e.g., http://192.168.1.17:30070).")
    parser.add_argument("--api_key", required=True, help="Your Paperless-ngx API key.")
    parser.add_argument("--title", help="(Optional) Title for the document.")
    parser.add_argument("--tags", help="(Optional) Comma-separated list of tags (e.g., 'invoice,paid').")
    parser.add_argument("--document_type", help="(Optional) Document type name (e.g., 'Invoice').")

    args = parser.parse_args()

    upload_document(args.file_path, args.host, args.api_key, args.title, args.tags, args.document_type)
