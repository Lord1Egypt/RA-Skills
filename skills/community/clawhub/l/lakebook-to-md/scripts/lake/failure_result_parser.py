def parse_failure_result(failure_list):
    if not failure_list:
        print("无下载失败项")
        return
    print(f"共 {len(failure_list)} 个下载失败项:")
    for item in failure_list:
        print(f"  {item}")
