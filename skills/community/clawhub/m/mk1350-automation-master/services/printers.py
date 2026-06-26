# 打印机配置文件
# 请根据你的实际网络打印机地址修改

NETWORK_PRINTERS = {
    # 示例：'办公室打印机': '\\\\192.168.1.100\\HP LaserJet'
    # 注意：Windows 网络打印机路径格式为 \\\\IP地址\\打印机名
    '默认打印机': 'YOUR_PRINTER_PATH_HERE',
}

# 可选：部门使用提示
DEPARTMENT_HINTS = {
    '默认打印机': '请修改为你的实际打印机路径',
}