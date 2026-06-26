# def test_query_room_levels_root(mock_run, api):
#     mock_run.return_value = {"items": []}

#     out = api.query_room_levels()

#     mock_run.assert_called_once_with(
#         "GET",
#         "vc/v1/room_levels",
#         params={"page_size": 100},
#     )
#     assert out == {"items": []}

import sys
from pathlib import Path

# 直接 `python scripts/test.py` 时 sys.path 首项是 scripts/，无法解析包名 `scripts`；
# 先把仓库根目录加入 path，再按包导入。
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from scripts.lark_cli import LarkAPI


def main():
    client = LarkAPI()
    out0 = client.query_room_levels(page_size=100, depth=2)
    out1 = client.search_rooms(room_level_id="omb_89fc6343fe615428da9da905ce69c7f0", page_size=100)
    print(out0)
    print(out1)


if __name__ == "__main__":
    main()
