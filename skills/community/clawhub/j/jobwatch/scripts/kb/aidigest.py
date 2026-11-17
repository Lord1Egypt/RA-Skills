"""AI Digest adapter（预留，未启用）。

将来与 AI Digest（https://github.com/ywc668/ai-digest）整合时实现：
它的 documents 表是 unified Document model（id/source_type/source_path/title/content/
metadata/document_type/created_at），与 JobWatcher 的 doc 字段一一对应，
source_type='web'、document_type='article' 即可直接入库。

两条实现路径（二选一）：
1. AI Digest 机器暴露一个小的 HTTP ingest endpoint，这里 POST 过去（双写）。
2. 定期把 runs/ 里的 Document JSONL rsync 过去批量导入。
"""


def upload_doc(filename, content_md):
    raise NotImplementedError("aidigest adapter: planned for next phase, see module docstring")
