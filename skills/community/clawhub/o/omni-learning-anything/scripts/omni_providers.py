"""Load only the selected provider; host tools remain the agent's responsibility."""
import importlib


def publish_document(root, manifest, target, receipt, checkpoint):
    modules = {'obsidian': 'omni_obsidian', 'notion': 'omni_notion', 'feishu': 'omni_feishu',
               'tencent': 'omni_tencent', 'dingtalk': 'omni_dingtalk'}
    module = importlib.import_module(modules[target['platform']])
    return module.publish(root, manifest, target, receipt, checkpoint)
