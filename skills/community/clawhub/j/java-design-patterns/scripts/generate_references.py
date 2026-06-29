#!/usr/bin/env python3
"""从 data/ 目录生成 references/ 下的参考文档"""
import json
import os
import re

DATA_DIR = os.path.expanduser("~/.claude/skills/java-design-patterns/data")
REFS_DIR = os.path.expanduser("~/.claude/skills/java-design-patterns/references")
SRC_FILE = os.path.expanduser(
    "~/.claude/projects/-Users-wufengsheng/48ef65f3-98db-4f7c-9d95-36c1815729f5/"
    "tool-results/mcp-firecrawl-mcp-firecrawl_crawl-1782351365733.txt"
)

CATEGORY_MAP = {
    'Architectural': 'architectural', 'Behavioral': 'behavioral',
    'Concurrency': 'concurrency', 'Creational': 'creational',
    'Data access': 'data-access', 'Functional': 'functional',
    'Integration': 'integration', 'Resilience': 'resilience',
    'Testing': 'testing', 'Messaging': 'messaging',
    'Performance optimization': 'performance-optimization',
    'Resource management': 'resource-management',
    'Idiom': 'idiom', 'Service Discovery': 'service-discovery',
    'Structural': 'structural',
}

# 中文名映射
ZH_NAMES = {
    "abstract-document": "抽象文档", "abstract-factory": "抽象工厂",
    "active-object": "活动对象", "actor-model": "Actor 模型",
    "acyclic-visitor": "无环访问者", "adapter": "适配器",
    "ambassador": "大使", "anti-corruption-layer": "防腐层",
    "arrange-act-assert": "3A 模式", "async-method-invocation": "异步方法调用",
    "backpressure": "背压", "balking": "犹豫",
    "bloc": "Bloc", "bridge": "桥接", "builder": "建造者",
    "business-delegate": "业务代表", "bytecode": "字节码", "caching": "缓存",
    "callback": "回调", "chain-of-responsibility": "责任链",
    "circuit-breaker": "断路器", "clean-architecture": "整洁架构",
    "client-session": "客户端会话", "collecting-parameter": "收集参数",
    "collection-pipeline": "集合管道", "combinator": "组合子",
    "command": "命令", "commander": "指挥官",
    "command-query-responsibility-segregation": "CQRS", "component": "组件",
    "composite": "组合", "composite-entity": "组合实体",
    "composite-view": "组合视图", "context-object": "上下文对象",
    "converter": "转换器", "curiously-recurring-template-pattern": "CRTP",
    "currying": "柯里化",
    "dao-factory": "DAO 工厂", "data-access-object": "DAO",
    "data-bus": "数据总线", "data-locality": "数据局部性",
    "data-mapper": "数据映射器", "data-transfer-object": "DTO",
    "decorator": "装饰器", "delegation": "委托",
    "dependency-injection": "依赖注入", "dirty-flag": "脏标记",
    "domain-model": "领域模型", "double-buffer": "双缓冲",
    "double-checked-locking": "双重检查锁定", "double-dispatch": "双分派",
    "dynamic-proxy": "动态代理", "event-aggregator": "事件聚合器",
    "event-based-asynchronous": "基于事件的异步",
    "event-driven-architecture": "事件驱动架构", "event-queue": "事件队列",
    "event-sourcing": "事件溯源", "execute-around": "环绕执行",
    "extension-objects": "扩展对象", "facade": "外观",
    "factory": "工厂", "factory-kit": "工厂套件",
    "factory-method": "工厂方法", "fanout-fanin": "扇出扇入",
    "feature-toggle": "特性开关", "filterer": "过滤器",
    "fluent-interface": "流式接口", "flux": "Flux",
    "flyweight": "享元", "front-controller": "前端控制器",
    "function-composition": "函数组合", "game-loop": "游戏循环",
    "gateway": "网关", "guarded-suspension": "守护挂起",
    "half-sync-half-async": "半同步半异步", "health-check": "健康检查",
    "hexagonal-architecture": "六边形架构", "identity-map": "标识映射",
    "immutable": "不可变", "intercepting-filter": "拦截过滤器",
    "interpreter": "解释器", "iterator": "迭代器",
    "layered-architecture": "分层架构", "lazy-loading": "延迟加载",
    "leader-election": "领导者选举", "leader-followers": "领导者跟随者",
    "lockable-object": "可锁定对象", "map-reduce": "MapReduce",
    "marker-interface": "标记接口", "master-worker": "主从模式",
    "mediator": "中介者", "memento": "备忘录",
    "metadata-mapping": "元数据映射",
    "microservices-aggregrator": "微服务聚合器",
    "microservices-api-gateway": "微服务 API 网关",
    "microservices-client-side-ui-composition": "客户端 UI 组合",
    "microservices-distributed-tracing": "分布式追踪",
    "microservices-idempotent-consumer": "幂等消费者",
    "microservices-log-aggregation": "日志聚合",
    "microservices-self-registration": "自注册",
    "model-view-controller": "MVC", "model-view-intent": "MVI",
    "model-view-presenter": "MVP", "model-view-viewmodel": "MVVM",
    "monad": "Monad", "money": "货币", "monitor": "监视器",
    "monolithic-architecture": "单体架构", "monostate": "单态",
    "multiton": "多例", "mute-idiom": "静默惯用法",
    "naked-objects": "裸对象", "notification": "通知",
    "null-object": "空对象", "object-mother": "对象母亲",
    "object-pool": "对象池", "observer": "观察者",
    "optimistic-offline-lock": "乐观离线锁",
    "page-controller": "页面控制器", "page-object": "页面对象",
    "parameter-object": "参数对象", "partial-response": "部分响应",
    "pipeline": "管道", "poison-pill": "毒丸",
    "polling-publisher": "轮询发布订阅",
    "presentation-model": "展示模型",
    "private-class-data": "私有类数据",
    "producer-consumer": "生产者消费者", "promise": "Promise",
    "property": "属性", "prototype": "原型", "proxy": "代理",
    "publish-subscribe": "发布订阅",
    "queue-based-load-leveling": "队列负载均衡",
    "rate-limiting-pattern": "限流", "reactor": "反应器",
    "registry": "注册表", "repository": "仓储",
    "resource-acquisition-is-initialization": "RAII",
    "retry": "重试", "role-object": "角色对象", "saga": "Saga",
    "separated-interface": "分离接口", "serialized-entity": "序列化实体",
    "serialized-lob": "序列化大对象",
    "servant": "仆人", "server-session": "服务器会话",
    "service-layer": "服务层", "service-locator": "服务定位器",
    "service-stub": "服务桩", "service-to-worker": "服务到工作者",
    "session-facade": "会话外观", "sharding": "分片",
    "single-table-inheritance": "单表继承",
    "singleton": "单例", "spatial-partition": "空间分区",
    "special-case": "特例", "specification": "规格",
    "state": "状态", "step-builder": "步骤建造者",
    "strangler": "绞杀者", "strategy": "策略",
    "subclass-sandbox": "子类沙箱",
    "table-inheritance": "表继承", "table-module": "表模块",
    "template-method": "模板方法", "templateview": "模板视图",
    "thread-pool-executor": "线程池执行器",
    "thread-specific-storage": "线程特定存储",
    "throttling": "节流", "tolerant-reader": "宽容读取器",
    "trampoline": "蹦床", "transaction-script": "事务脚本",
    "twin": "双生子", "type-object": "类型对象",
    "unit-of-work": "工作单元", "update-method": "更新方法",
    "value-object": "值对象", "version-number": "版本号",
    "view-helper": "视图助手", "virtual-proxy": "虚拟代理",
    "visitor": "访问者",
}

# 读取源 JSON 获取 tags
with open(SRC_FILE, 'r', encoding='utf-8') as f:
    raw = f.read()
cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', raw)
src_data = json.loads(cleaned)

# 建立 url -> tags 的映射
url_tags = {}
url_category = {}
url_description = {}
for e in src_data.get('data', []):
    meta = e.get('metadata', {})
    url = meta.get('sourceURL', '') or meta.get('url', '')
    if not url:
        continue
    # 提取 tags
    tags = meta.get('article:tag', []) or []
    keywords = meta.get('keywords', '')
    if keywords and not tags:
        tags = [t.strip() for t in keywords.split(',')]
    url_tags[url] = tags
    url_category[url] = meta.get('articleSection', '')
    url_description[url] = meta.get('description', '') or meta.get('ogDescription', '')

# 从 data/ 目录读取所有 md 文件
count = 0
for filename in sorted(os.listdir(DATA_DIR)):
    if not filename.endswith('.md'):
        continue
    slug = filename[:-3]  # 去掉 .md
    filepath = os.path.join(DATA_DIR, filename)
    url = f"https://java-design-patterns.com/patterns/{slug}/"

    # 确定分类
    cat_name = url_category.get(url, '')
    cat_dir = CATEGORY_MAP.get(cat_name, 'uncategorized')
    if cat_dir == 'uncategorized':
        # 从 mapping 文件查找
        with open(os.path.join(DATA_DIR, 'category-mapping.txt')) as mf:
            for line in mf:
                if line.strip().endswith(f'|{slug}'):
                    cat_dir = line.split('|')[0]
                    break

    # 读取内容
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 清理内容
    lines = content.split('\n')
    cleaned_lines = []
    skip = True
    for line in lines:
        if skip and ('Skip to main content' in line or line.strip().startswith('[Skip')):
            skip = False
            continue
        skip = False
        line = line.replace('\\#', '#')
        cleaned_lines.append(line)
    content = '\n'.join(cleaned_lines).strip()

    # 提取模式名称
    title_match = re.search(r'^# (.+?) Pattern in Java', content, re.MULTILINE)
    if not title_match:
        title_match = re.search(r'^# (.+?)(?: \| Java Design Patterns)?$', content, re.MULTILINE)
    display_name = title_match.group(1) if title_match else slug.replace('-', ' ').title()

    # 移除原 h1 标题
    content = re.sub(r'^# .+?\n\n', '', content, count=1)

    # 重新添加双语标题
    zh_name = ZH_NAMES.get(slug, '')
    title_line = f"# {display_name}"
    if zh_name:
        title_line += f" {zh_name}模式"

    # 构建 frontmatter
    tags = url_tags.get(url, [])
    tags_str = ', '.join(tags[:8])  # 最多8个标签
    desc = url_description.get(url, f'{display_name} 设计模式 Java 实现')
    # 截断过长的描述
    if len(desc) > 200:
        desc = desc[:197] + '...'

    frontmatter = f"""---
name: "{slug}"
description: "{display_name}{' ' + zh_name if zh_name else ''} -- {cat_name}设计模式。{desc[:150]}"
url: "{url}"
category: "{cat_dir}"
tags: [{tags_str}]
---

{title_line}

> 官方文档: {url}
> 分类: {cat_name} ({cat_dir})
{f'> 标签: {tags_str}' if tags_str else ''}

{content}
"""

    # 写入 reference 文件
    ref_dir = os.path.join(REFS_DIR, cat_dir)
    os.makedirs(ref_dir, exist_ok=True)
    ref_path = os.path.join(ref_dir, f"{slug}.md")
    with open(ref_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter)

    count += 1

print(f"Generated: {count} reference files")

# 统计各分类文件数
for d in sorted(os.listdir(REFS_DIR)):
    full = os.path.join(REFS_DIR, d)
    if os.path.isdir(full):
        cnt = len([f for f in os.listdir(full) if f.endswith('.md')])
        print(f"  {d}: {cnt}")
