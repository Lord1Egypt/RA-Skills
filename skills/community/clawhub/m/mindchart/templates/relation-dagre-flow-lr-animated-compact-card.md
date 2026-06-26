infographic relation-dagre-flow-lr-animated-compact-card
data
  title 内容发布审核流程
  desc 创作者提交内容到发布上线的标准链路（含驳回回路）
  nodes
    - label 开始
      id start
      desc 创作者准备发布
      icon mingcute/play-circle-line
    - label 提交内容
      id submit
      desc 填写标题、正文、素材
      icon mingcute/edit-line
    - label 机器审核
      id auto
      desc 涉政涉黄/版权/低质检测
      icon mingcute/robot-line
    - label 人工复审
      id manual
      desc 边界内容进一步判断
      icon mingcute/user-search-line
    - label 发布上线
      id publish
      desc 内容对外可见
      icon mingcute/send-line
    - label 驳回修改
      id reject
      desc 退回并给出原因
      icon mingcute/close-circle-line
    - label 结束
      id end
      desc 流程闭环
      icon solar/flag-linear
  relations
    start -> submit
    submit -> auto
    auto -> publish
    auto -> manual
    auto -> reject
    manual -> publish
    manual -> reject
    reject -> submit
    publish -> end
theme light
  palette antv