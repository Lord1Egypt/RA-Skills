# DEPRECATED - 此文件已废弃
#
# 自适应轮询功能已迁移到 adaptive_poller.py
# auto_poller.py 在 v2.0 中不再使用，请使用：
#
#   from adaptive_poller import AdaptivePoller
#   poller = AdaptivePoller()
#   poller.on_signal(lambda sig: print(f"收到: {sig['type']}"))
#   poller.start()
#
# 如有部署脚本引用本文件，请更新为 adaptive_poller.py
