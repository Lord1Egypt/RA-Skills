"""
filecontent_get.py——打开文件获取php代码
"""
import re

def readfile_code_to_list(file_path):
	with open(file_path,'r') as f:
		lines=[]
		for line in f:
			line=line.rstrip('\n')#去除行尾换行符
			line=re.sub(r'//.*|#.*','',line)#处理单行注释（//和#）
			line=re.sub(r'/\*.*?\*/','',line)#处理行内的多行注释（/*...*/）
			line=line.strip()#去除处理后的行首尾空白
			if not line and line != '':
				line=''#如果处理后是空字符串但原行不是空行，保留空字符串
			lines.append(line)
		return lines

def readfile_bintoutf8_to_list(file_path):#以utf8强行打开文件进而寻找图片等文件中的恶意内容
	with open(file_path,'rb') as file:
		lines=[]
		for line in file:
			try:
				decoded_line=line.decode('utf-8',errors='ignore')
				lines.append(decoded_line)
			except Exception as e:
				print(f"解码失败:{e}")
				lines.append(line)
		return lines