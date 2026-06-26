import re

def parse_filename(path):
    filename = path.split("/")[-1]

    match = re.match(r"(.+)-(\d+)-第(\d+)次作业\.zip", filename)

    if match:
        name = match.group(1)
        student_id = match.group(2)
        hw_id = int(match.group(3))
        return name, student_id, hw_id

    return None