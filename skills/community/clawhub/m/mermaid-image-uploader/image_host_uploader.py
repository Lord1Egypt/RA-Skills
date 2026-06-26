"""
Image Host Uploader Module
Supports multiple free image hosts
"""
import requests
import os
from typing import Optional


class ImageHostUploader:
    """Image Host Uploader"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def upload_to_freeimage(self, image_path: str) -> Optional[str]:
        """
        Upload to FreeImage.host (free, no API key needed)

        Args:
            image_path: Image file path

        Returns:
            Image URL or None
        """
        try:
            url = "https://freeimage.host/api/1/upload"

            with open(image_path, 'rb') as f:
                files = {'source': f}
                data = {'key': '6d207e02198a847aa98d0a2a901485a5'}  # public key for demo

                response = requests.post(url, files=files, data=data, timeout=30)

                if response.status_code == 200:
                    result = response.json()
                    if result.get('status_code') == 200:
                        return result['image']['url']

        except Exception as e:
            print(f"FreeImage upload failed: {e}")

        return None

    def upload_to_postimages(self, image_path: str) -> Optional[str]:
        """
        Upload to Postimages (free, no API key needed)

        Args:
            image_path: Image file path

        Returns:
            Image URL or None
        """
        try:
            url = "https://postimages.org/json"

            with open(image_path, 'rb') as f:
                files = {'file': f}
                data = {'ui': '1'}

                response = requests.post(url, files=files, data=data, timeout=30)

                if response.status_code == 200:
                    result = response.json()
                    if 'url' in result:
                        return result['url']

        except Exception as e:
            print(f"Postimages upload failed: {e}")

        return None

    def upload_to_imgur(self, image_path: str, client_id: str) -> Optional[str]:
        """
        Upload to Imgur (requires Client ID)

        Args:
            image_path: Image file path
            client_id: Imgur Client ID

        Returns:
            Image URL or None
        """
        try:
            url = "https://api.imgur.com/3/image"

            headers = {'Authorization': f'Client-ID {client_id}'}

            with open(image_path, 'rb') as f:
                files = {'image': f}

                response = requests.post(url, headers=headers, files=files, timeout=30)

                if response.status_code == 200:
                    result = response.json()
                    if result.get('success'):
                        return result['data']['link']

        except Exception as e:
            print(f"Imgur upload failed: {e}")

        return None

    def upload(self, image_path: str, image_host: str = 'freeimage', **kwargs) -> Optional[str]:
        """
        Upload image to specified host

        Args:
            image_path: Image file path
            image_host: Image host name (freeimage, postimages, imgur)
            **kwargs: Other parameters (api_key, client_id)

        Returns:
            Image URL or None
        """
        if not os.path.exists(image_path):
            print(f"File not found: {image_path}")
            return None

        print(f"Uploading to {image_host}...")

        if image_host == 'freeimage':
            return self.upload_to_freeimage(image_path)
        elif image_host == 'postimages':
            return self.upload_to_postimages(image_path)
        elif image_host == 'imgur':
            client_id = kwargs.get('client_id', kwargs.get('api_key'))
            if not client_id:
                print("Imgur requires Client ID")
                return None
            return self.upload_to_imgur(image_path, client_id)
        else:
            print(f"Unsupported image host: {image_host}")
            return None


# Simple test
if __name__ == '__main__':
    print("Image Host Uploader loaded successfully")
    print("Supported hosts: freeimage, postimages, imgur")
