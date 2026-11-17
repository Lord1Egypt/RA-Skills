# -*- coding: utf-8 -*-
"""
jscontent_get.py —— JS 文件内容读取层。

以二进制强行按 UTF-8 解码读取(可扫图片/二进制里藏的 JS payload),
去除行首尾空白,返回行列表。
"""
def readfile_bintoutf8_to_list(file_path):#以utf8强行打开文件进而寻找图片等文件中的恶意内容
	with open(file_path,'rb') as file:
		lines=[]
		for line in file:
			decoded_line=line.decode('utf-8',errors='ignore')
			lines.append(decoded_line.rstrip('\n'))
		return lines
