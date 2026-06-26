import os.path
import tarfile

__EMPTY_ = 0x00


def unpack_lake_book_file(lake_file, extract_to):
    """解包 .lakebook 文件（tar 格式）到指定目录"""
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)
    with tarfile.open(lake_file, "r") as tar_ref:
        tar_ref.extractall(extract_to)
    secondary_dir_name = get_lake_book_dir_name(lake_book_path=lake_file)
    return os.path.join(extract_to, secondary_dir_name)


def get_lake_book_dir_name(lake_book_path):
    """从 lakebook 文件头读取次级目录名"""
    with open(lake_book_path, "rb+") as f:
        head_block_byte = f.read(512)
        file_name = get_file_name(head_block_byte)
        name = os.path.split(file_name)[0]
        return name


def get_file_name(head_block):
    """从文件头字节中提取文件名"""
    file_name_part_byte = head_block[:100]
    file_name_byte = []
    for b in file_name_part_byte:
        if b == __EMPTY_:
            break
        else:
            file_name_byte.append(b)
    return bytes(file_name_byte).decode("utf-8")
