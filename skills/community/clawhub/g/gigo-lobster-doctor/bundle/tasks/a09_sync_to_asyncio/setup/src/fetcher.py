import time


def fetch_one(url_id):
    time.sleep(0.05)
    return f"item-{url_id}"


def fetch_all(ids):
    return [fetch_one(i) for i in ids]
