import os

def get_media_directory():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "videos")

def get_media_files():
    directory = get_media_directory()
    
    media_extensions = {'.mp4'}
    media_files = []
    
    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                ext = os.path.splitext(item)[1].lower()
                if ext in media_extensions:
                    media_files.append(item_path)
    except OSError as e:
        return media_files
    
    media_files.sort(key=lambda a: a.lower())
    
    return media_files
