# Local File Reader

读取本地文件内容（支持 .txt, .md, .json, .docx, .pdf 等）

## 触发条件
用户提到：读取文件、查看文件、打开文件、读一下 xxx 文件

## 用法
- 读取：read <文件路径>
- 总结：summarize <文件路径>
- 搜索：search <关键词> <文件路径>

## 限制
- 只能读取工作区和用户明确授权的路径
- 大文件（>10MB）会拒绝