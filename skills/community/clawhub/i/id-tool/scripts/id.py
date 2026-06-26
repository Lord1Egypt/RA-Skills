#!/usr/bin/env python3
import os, pwd, grp
uid = os.getuid()
euid = os.geteuid()
gid = os.getgid()
print(f"uid={uid}({pwd.getpwuid(uid).pw_name}) gid={gid}({grp.getgrgid(gid).gr_name})")
