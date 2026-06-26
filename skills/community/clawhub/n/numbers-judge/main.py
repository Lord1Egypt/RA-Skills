import sys

if __name__ == "__main__":
    # 打印所有参数
    print("所有参数列表：", sys.argv)
    content = sys.argv[1]
    spit_str = sys.argv[2]
    str_arr = content.split(spit_str)
    not_num = []
    for s in str_arr:
        try:
            int(s)
        except Exception as e:
            not_num.append(s)
    print(",".join(not_num))
