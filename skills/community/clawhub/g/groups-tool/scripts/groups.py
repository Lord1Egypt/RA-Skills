#!/usr/bin/env python3
import os, grp
for g in grp.getgrall():
    if os.getlogin() in g.gr_mem:
        print(g.gr_name)
