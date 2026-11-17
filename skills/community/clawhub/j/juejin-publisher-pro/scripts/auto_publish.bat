@echo off
rem 定时发布驱动包装——把下行 cd 改成你的项目根目录
cd /d D:\your\blog
uv run auto_publish.py --daily-limit 2 --min-gap-hours 1 --task-names Blog_morning,Blog_evening >> _wf\auto_publish.log 2>&1
