/**
 * project-timeline-data.js — 项目时间线配置模板
 *
 * 使用方法（3 步）：
 * 1. 复制本文件到你的项目目录
 * 2. 修改下面的 PROJECT_CONFIG 数据（大多数字段有注释说明）
 * 3. 在 project-timeline.html 之前引入：
 *    <script src="project-timeline-data.js"></script>
 *
 * 页面会自动读取 window.PROJECT_CONFIG 并渲染所有内容。
 */

// ===================== 最简配置示例 =====================
// 下面是一个最小化的完整配置（覆盖所有模块）
// 复制后只需改日期和标题即可使用

window.PROJECT_CONFIG = {

  // ========== 1. 基本信息 ==========
  projectName:    '我的项目',          // 项目名称（Hero 标题）
  projectSubtitle: '产品设计协作',     // 副标题
  status:         '进行中',            // '进行中' | '已完成' | '已发布'

  // 时间范围
  startDate:  '2026.04.01',           // 项目开始日期
  endDate:    '2026.06.30',           // 项目结束日期
  totalWeeks: 13,                     // 总周数

  // Hero 区域高亮文案
  heroBadge:  '正在进行中',           // 状态徽章文字
  heroPhase:  '当前阶段：设计和开发中', // 阶段说明

  // ========== 2. Overview 四宫格 ==========
  // 显示在 Hero 下方的 4 个关键日期卡片
  overview: [
    { date: '4.15', label: '交互稿完成', color: 'blue'   },
    { date: '4.20', label: '视觉稿完成', color: 'purple' },
    { date: '5.01', label: '开发完成',   color: 'cyan'  },
    { date: '5.15', label: '正式发布',   color: 'rose'  }
  ],
  // color 可选：blue / purple / green / cyan / amber / rose

  // ========== 3. 关键节点（Key Nodes）==========
  // 数量任意，每个节点可折叠展开
  // 自动状态判断（基于今天 2026.04.17）：
  //   today — 日期等于今天
  //   done  — 日期 < 今天（自动加 ✓）
  //   soon  — 日期 > 今天 且 距离 ≤ 3 天
  //   later — 日期 > 今天 且 距离 > 3 天
  keyNodes: [

    {
      date:    '4.10',
      title:   '需求评审',
      subtitle:'4.08 → 4.10 · PRD 对齐 + 技术方案确认',
      color:   'blue',
      badge:   '规划',
      open:    false,                  // true=默认展开
      active:  false,                  // true=显示呼吸灯（当前进行中）
      detail: [
        { subLabel: 'PRD 评审通过',     subDate: '4-10' },
        { subLabel: '技术方案确认',     subDate: '4-10' }
      ]
    },

    {
      date:    '4.15',
      title:   '交互稿交付',
      subtitle:'4.10 → 4.15 · 全模块交互稿完成',
      color:   'blue',
      badge:   '交互',
      open:    false,
      active:  false,
      detail: [
        { subLabel: '首页交互稿',       subDate: '4-13' },
        { subLabel: '核心流程交互稿',   subDate: '4-15' }
      ]
    },

    {
      date:    '4.20',
      title:   '视觉稿交付',
      subtitle:'4.15 → 4.20 · 设计稿全部完成',
      color:   'purple',
      badge:   '视觉',
      open:    false,
      active:  false,
      detail: [
        { subLabel: '设计规范定稿',     subDate: '4-18' },
        { subLabel: '全模块视觉稿',     subDate: '4-20' }
      ]
    },

    {
      date:    '5.01',
      title:   '开发完成',
      subtitle:'4.21 → 5.01 · 前后端联调完成',
      color:   'green',
      badge:   '开发',
      open:    false,
      active:  false,
      detail: [
        { subLabel: '后端接口完成',     subDate: '4-25' },
        { subLabel: '前端开发完成',     subDate: '4-28' },
        { subLabel: '联调通过',         subDate: '5-01' }
      ]
    },

    {
      date:    '5.15',
      title:   '正式发布',
      subtitle:'灰度上线 → 全量发布',
      color:   'rose',
      badge:   '发布',
      open:    false,
      active:  false,
      detail: []
    }

    // 添加更多节点：复制上面的结构块即可
  ],

  // ========== 4. Gantt 甘特图 ==========
  // ganttStart / ganttEnd：日期范围（只支持同一年内整数日期）
  //   日期 = 月份 + 日期，4.10 = 4月10日，范围 1-31
  // ganttColorMap：类型 → 颜色标签映射
  // ganttData：[模块名, [{t:类型, f:起始日, to:结束日}, ...]]
  //   类型：ix=交互(蓝)  vis=视觉(紫)  fe=前端(绿)  be=后端(青)  tool=工具(橙)  test=测试(粉)

  ganttStart: 8,    // 4月8日
  ganttEnd:   22,   // 4月22日

  ganttColorMap: {
    ix:   { label: '交互', cls: 'ix'   },
    vis:  { label: '视觉', cls: 'vis'  },
    fe:   { label: '前端', cls: 'fe'   },
    be:   { label: '后端', cls: 'be'   },
    tool: { label: '工具', cls: 'tool' },
    test: { label: '测试', cls: 'test' }
  },

  ganttData: [
    ['首页',       [{t:'ix',  f:8,  to:11}, {t:'vis', f:11, to:14}, {t:'fe', f:14, to:18}]],
    ['核心流程',   [{t:'ix',  f:8,  to:12}, {t:'vis', f:12, to:16}, {t:'fe', f:16, to:20}, {t:'be', f:8,  to:15}]],
    ['个人中心',   [{t:'ix',  f:10, to:13}, {t:'vis', f:13, to:16}, {t:'fe', f:17, to:20}]],
    ['测试',       [{t:'test',f:20, to:22}]]
  ],
  // 添加更多模块：复制 ['模块名', [{t:'类型', f:起始, to:结束}]] 格式即可

  // ========== 5. 待办清单（To-Do） ==========
  // 按阶段/周分组，checkbox 切换 done 状态
  // tag 类型：ix=交互 / vis=视觉 / fe=前端 / be=后端 / plan=规划 / collab=协作 / tool=工具 / test=测试

  todos: [
    {
      period: '4.08 — 4.12 第一周',
      count:  4,
      items: [
        { text: 'PRD 评审',           tag: 'plan',   done: true  },
        { text: '技术方案设计',       tag: 'plan',   done: true  },
        { text: '首页交互稿',        tag: 'ix',     done: true  },
        { text: '后端接口定义',      tag: 'be',     done: false }
      ]
    },
    {
      period: '4.13 — 4.19 第二周',
      count:  4,
      items: [
        { text: '核心流程交互稿',    tag: 'ix',     done: false },
        { text: '视觉设计',          tag: 'vis',    done: false },
        { text: '后端接口开发',      tag: 'be',     done: false },
        { text: '前端开发',          tag: 'fe',     done: false }
      ]
    },
    {
      period: '4.20 — 4.30 第三、四周',
      count:  3,
      items: [
        { text: '前后端联调',        tag: 'collab', done: false },
        { text: '测试',             tag: 'test',   done: false },
        { text: '修复 Bug',         tag: 'tool',   done: false }
      ]
    }
    // 添加更多周：复制上面的结构块即可
  ],

  // ========== 6. Extras 关注事项（可选）==========
  // 可放测试计划 / 当前状态 / 风险等，每个 card 格式自由

  extras: {
    testing: {
      label:   '测试计划',
      content: '4.20 开始 QA 测试，4.25 之前完成首轮测试'
    },
    status: {
      label:   '当前状态',
      type:    'ok',                  // ok=绿色 / info=蓝色 / warn=黄色 / 空=灰
      content: '需求已完成，交互稿进行中'
    }
    // 可添加更多 card：如 risk、collab、notes 等
  }

};
