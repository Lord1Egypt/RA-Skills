# 🕸️ 宠物关系图谱 (Pet Relation Graph)

**版本**：V1.0  
**创建日期**：2026-04-11  
**最后更新**：2026-04-11  
**大小**：15.7KB

---

## 一、概述

宠物关系图谱是 Investment Buddy 的**社交网络可视化**系统，使用 ECharts + Neo4j 实现宠物关系的存储、查询和可视化。

### 1.1 设计目标

- 🕸️ **关系可视化**：直观展示宠物间的关系网络
- 🔍 **图查询**：支持复杂关系查询和推理
- 📊 **动态演化**：关系随用户互动动态变化
- 🎨 **交互体验**：用户可探索、缩放、筛选

### 1.2 技术架构

```
┌─────────────────────────────────────────────────────┐
│                  宠物关系图谱系统                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────┐         ┌──────────────┐        │
│  │   Neo4j      │         │    ECharts   │        │
│  │  (图数据库)   │  ←───→  │  (可视化)    │        │
│  └──────────────┘         └──────────────┘        │
│         ↑                          ↑               │
│         │                          │               │
│  ┌──────────────┐         ┌──────────────┐        │
│  │   Graph API  │         │  Frontend    │        │
│  │  (查询接口)   │  ←───→  │   (交互)     │        │
│  └──────────────┘         └──────────────┘        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 二、图数据模型

### 2.1 节点类型 (Node Types)

```cypher
// 宠物节点
(:Pet {
    pet_id: "songguo_001",
    name: "松果",
    species: "松鼠",
    investment_style: "value",
    risk_tolerance: "conservative",
    communication_style: "warm",
    proactivity_level: 40,
    intervention_threshold: 70,
    avatar_url: "/images/pets/songguo.png",
    created_at: datetime()
})

// 用户节点
(:User {
    user_id: "user_12345",
    nickname: "燃冰",
    investment_personality: "稳健价值型",
    risk_score: 45,
    knowledge_level: 60,
    registered_at: datetime()
})

// 投资概念节点
(:Concept {
    concept_id: "value_investing",
    name: "价值投资",
    category: "investment_style",
    description: "以低于内在价值的价格买入",
    related_pets: ["songguo", "boshi"]
})

// 市场事件节点
(:MarketEvent {
    event_id: "evt_20260411_001",
    type: "market_crash",
    date: date("2026-04-11"),
    description: "市场大跌 3%",
    impact_level: "high"
})
```

### 2.2 关系类型 (Relationship Types)

```cypher
// 宠物 - 宠物关系
(:Pet)-[:COMPATIBLE_WITH {strength: 0.8}]->(:Pet)
(:Pet)-[:OPPOSITE_TO {strength: 0.6}]->(:Pet)
(:Pet)-[:MENTORS {since: datetime()}]->(:Pet)
(:Pet)-[:COLLABORATES_WITH {frequency: "daily"}]->(:Pet)

// 用户 - 宠物关系
(:User)-[:OWNS {since: datetime(), intimacy: 75}]->(:Pet)
(:User)-[:INTERACTS_WITH {count: 156, last_at: datetime()}]->(:Pet)
(:User)-[:PREFERS {reason: "warm_style"}]->(:Pet)

// 宠物 - 概念关系
(:Pet)-[:EXPERT_IN {proficiency: 0.9}]->(:Concept)
(:Pet)-[:TEACHES {level: "beginner"}]->(:Concept)

// 宠物 - 事件关系
(:Pet)-[:RESPONDED_TO {response_time: 300}]->(:MarketEvent)
(:Pet)-[:ANALYZED {analysis_quality: 0.85}]->(:MarketEvent)
```

### 2.3 完整图 Schema

```cypher
// 节点标签
:Pet
:User
:Concept
:MarketEvent
:Task
:Interaction

// 关系类型
COMPATIBLE_WITH      // 宠物兼容
OPPOSITE_TO          // 宠物对立
MENTORS              // 宠物指导
COLLABORATES_WITH    // 宠物协作
OWNS                 // 用户拥有
INTERACTS_WITH       // 用户互动
PREFERS              // 用户偏好
EXPERT_IN            // 宠物专长
TEACHES              // 宠物教学
RESPONDED_TO         // 宠物响应
ANALYZED             // 宠物分析
TRIGGERED            // 事件触发
COMPLETED            // 任务完成
```

---

## 三、Neo4j 图数据库

### 3.1 数据库初始化

```cypher
// 创建索引
CREATE INDEX pet_id_index IF NOT EXISTS FOR (p:Pet) ON (p.pet_id);
CREATE INDEX user_id_index IF NOT EXISTS FOR (u:User) ON (u.user_id);
CREATE INDEX concept_id_index IF NOT EXISTS FOR (c:Concept) ON (c.concept_id);

// 创建约束
CREATE CONSTRAINT pet_id_unique IF NOT EXISTS FOR (p:Pet) REQUIRE p.pet_id IS UNIQUE;
CREATE CONSTRAINT user_id_unique IF NOT EXISTS FOR (u:User) REQUIRE u.user_id IS UNIQUE;
```

### 3.2 数据导入脚本

```python
from neo4j import GraphDatabase

class PetGraphDB:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def create_pet(self, pet_data):
        """创建宠物节点"""
        with self.driver.session() as session:
            session.execute_write(self._create_pet_tx, pet_data)
    
    @staticmethod
    def _create_pet_tx(tx, pet_data):
        query = """
        CREATE (p:Pet {
            pet_id: $pet_id,
            name: $name,
            species: $species,
            investment_style: $investment_style,
            risk_tolerance: $risk_tolerance,
            communication_style: $communication_style,
            proactivity_level: $proactivity_level,
            intervention_threshold: $intervention_threshold,
            avatar_url: $avatar_url,
            created_at: datetime()
        })
        RETURN p
        """
        return tx.run(query, **pet_data)
    
    def create_relationship(self, from_pet, to_pet, rel_type, properties):
        """创建宠物关系"""
        with self.driver.session() as session:
            session.execute_write(
                self._create_relationship_tx,
                from_pet, to_pet, rel_type, properties
            )
    
    @staticmethod
    def _create_relationship_tx(tx, from_pet, to_pet, rel_type, properties):
        query = f"""
        MATCH (a:Pet {{pet_id: $from_pet}})
        MATCH (b:Pet {{pet_id: $to_pet}})
        MERGE (a)-[r:{rel_type}]->(b)
        SET r += $properties
        RETURN r
        """
        return tx.run(query, from_pet=from_pet, to_pet=to_pet, properties=properties)
    
    def close(self):
        self.driver.close()
```

### 3.3 核心查询

#### 查询 1：查找兼容宠物

```cypher
// 查找与指定宠物兼容的其他宠物
MATCH (p1:Pet {pet_id: $pet_id})-[r:COMPATIBLE_WITH]->(p2:Pet)
WHERE r.strength > 0.7
RETURN p2.pet_id, p2.name, r.strength
ORDER BY r.strength DESC
LIMIT 5
```

#### 查询 2：查找宠物协作路径

```cypher
// 查找两只宠物之间的协作路径
MATCH path = (p1:Pet {pet_id: $pet_id_1})-[*1..3]-(p2:Pet {pet_id: $pet_id_2})
WHERE ALL(rel IN relationships(path) 
    WHERE type(rel) IN ['COMPATIBLE_WITH', 'COLLABORATES_WITH', 'MENTORS'])
RETURN path
LIMIT 10
```

#### 查询 3：用户宠物推荐

```cypher
// 基于用户性格推荐宠物
MATCH (u:User {user_id: $user_id})
MATCH (p:Pet)
WHERE 
    (p.investment_style = u.investment_personality_style) OR
    (p.risk_tolerance = u.risk_tolerance)
WITH p, 
    CASE 
        WHEN p.investment_style = u.investment_personality_style THEN 0.5 
        ELSE 0 END +
    CASE 
        WHEN p.risk_tolerance = u.risk_tolerance THEN 0.5 
        ELSE 0 END AS compatibility_score
RETURN p.pet_id, p.name, compatibility_score
ORDER BY compatibility_score DESC
LIMIT 3
```

#### 查询 4：宠物关系网络分析

```cypher
// 分析宠物关系网络
MATCH (p:Pet)-[r]-(other:Pet)
WITH p, count(other) as connection_count, avg(r.strength) as avg_strength
RETURN 
    p.pet_id, 
    p.name, 
    connection_count, 
    avg_strength,
    CASE 
        WHEN connection_count > 8 THEN 'highly_connected'
        WHEN connection_count > 4 THEN 'moderately_connected'
        ELSE 'low_connected'
    END as connectivity_level
ORDER BY connection_count DESC
```

#### 查询 5：宠物社区发现

```cypher
// 使用 Louvain 算法发现宠物社区
CALL gds.louvain.stream({
    nodeProjection: 'Pet',
    relationshipProjection: {
        COMPATIBLE: {
            type: 'COMPATIBLE_WITH',
            orientation: 'UNDIRECTED',
            properties: 'strength'
        }
    },
    relationshipWeightProperty: 'strength'
})
YIELD nodeId, communityId
RETURN gds.util.asNode(nodeId).pet_id, communityId
ORDER BY communityId
```

---

## 四、ECharts 可视化

### 4.1 基础关系图配置

```javascript
// ECharts 关系图配置
const option = {
    title: {
        text: '宠物关系图谱',
        subtext: '12 只宠物的性格互补与协作网络',
        top: 'bottom',
        left: 'right'
    },
    tooltip: {
        formatter: function (x) {
            return x.data.name + '<br/>' + 
                   '投资风格：' + x.data.investment_style + '<br/>' +
                   '风险偏好：' + x.data.risk_tolerance + '<br/>' +
                   '主动性：' + x.data.proactivity_level;
        }
    },
    legend: [{
        data: ['价值型', '成长型', '趋势型', '防御型', '灵活型'],
        selected: {
            '价值型': true,
            '成长型': true,
            '趋势型': true,
            '防御型': true,
            '灵活型': true
        }
    }],
    animationDuration: 1500,
    animationEasingUpdate: 'quinticInOut',
    series: [
        {
            name: '宠物关系',
            type: 'graph',
            layout: 'force',
            data: petNodes,
            links: petLinks,
            categories: petCategories,
            roam: true,
            label: {
                show: true,
                position: 'right',
                formatter: '{b}'
            },
            edgeSymbol: ['circle', 'arrow'],
            edgeSymbolSize: [4, 10],
            edgeLabel: {
                fontSize: 10
            },
            force: {
                repulsion: 200,
                edgeLength: [100, 300],
                gravity: 0.1
            },
            lineStyle: {
                color: 'source',
                curveness: 0.3,
                width: 1.5
            },
            emphasis: {
                focus: 'adjacency',
                lineStyle: {
                    width: 3
                }
            }
        }
    ]
};

// 宠物节点数据
const petNodes = [
    {
        id: 'songguo',
        name: '🐿️ 松果',
        symbolSize: 60,
        investment_style: 'value',
        risk_tolerance: 'conservative',
        proactivity_level: 40,
        category: 0, // 价值型
        draggable: true
    },
    {
        id: 'manman',
        name: '🐢 慢慢',
        symbolSize: 55,
        investment_style: 'long_term',
        risk_tolerance: 'balanced',
        proactivity_level: 50,
        category: 0,
        draggable: true
    },
    // ... 其他宠物
];

// 宠物关系数据
const petLinks = [
    {
        source: 'songguo',
        target: 'lieshou',
        value: '对立互补',
        symbolSize: 10,
        lineStyle: {
            color: '#ff6b6b',
            width: 2
        }
    },
    {
        source: 'songguo',
        target: 'boshi',
        value: '协作互补',
        symbolSize: 10,
        lineStyle: {
            color: '#51cf66',
            width: 2
        }
    },
    // ... 其他关系
];

// 宠物分类
const petCategories = [
    { name: '价值型' },
    { name: '成长型' },
    { name: '趋势型' },
    { name: '防御型' },
    { name: '灵活型' }
];
```

### 4.2 交互式功能

```javascript
// 点击节点高亮
chart.on('click', function (params) {
    if (params.dataType === 'node') {
        // 高亮相邻节点
        const nodeId = params.data.id;
        highlightAdjacentNodes(nodeId);
        
        // 显示宠物详情
        showPetDetail(nodeId);
    }
});

// 拖拽更新
chart.on('dragend', function (params) {
    if (params.dataType === 'node') {
        // 保存新位置
        saveNodePosition(params.data.id, params.data.x, params.data.y);
    }
});

// 缩放
chart.on('mousewheel', function (params) {
    // 动态调整标签显示
    updateLabelVisibility(params.zoom);
});
```

### 4.3 力导向布局优化

```javascript
// 自定义力导向布局
const forceLayout = {
    // 斥力（节点间排斥）
    repulsion: 300,
    
    // 引力（边的拉力）
    edgeLength: function (source, target) {
        // 关系强度越高，距离越近
        const strength = getRelationshipStrength(source, target);
        return 100 + (1 - strength) * 200;
    },
    
    // 重力（向中心聚集）
    gravity: 0.1,
    
    // 节点大小基于重要性
    nodeSize: function (node) {
        return 40 + node.proactivity_level * 0.4;
    }
};
```

---

## 五、关系图谱应用场景

### 5.1 宠物匹配推荐

```python
class PetMatcher:
    def __init__(self, graph_db):
        self.db = graph_db
    
    def recommend_pets(self, user_id, top_k=3):
        """为用户推荐最匹配的宠物"""
        
        # 1. 获取用户性格
        user = self.get_user_profile(user_id)
        
        # 2. 查询兼容宠物
        query = """
        MATCH (u:User {user_id: $user_id})
        MATCH (p:Pet)
        WHERE 
            (p.investment_style = $invest_style) OR
            (p.risk_tolerance = $risk_tol) OR
            (p.communication_style = $comm_style)
        WITH p, 
            CASE WHEN p.investment_style = $invest_style THEN 0.4 ELSE 0 END +
            CASE WHEN p.risk_tolerance = $risk_tol THEN 0.3 ELSE 0 END +
            CASE WHEN p.communication_style = $comm_style THEN 0.3 ELSE 0 END 
            AS score
        RETURN p, score
        ORDER BY score DESC
        LIMIT $top_k
        """
        
        result = self.db.run(query, 
            user_id=user_id,
            invest_style=user['investment_style'],
            risk_tol=user['risk_tolerance'],
            comm_style=user['communication_style'],
            top_k=top_k
        )
        
        return [record['p'] for record in result]
```

### 5.2 宠物辩论场景

```python
class PetDebate:
    def __init__(self, graph_db):
        self.db = graph_db
    
    def select_debaters(self, topic, user_pets):
        """为辩论话题选择合适的宠物"""
        
        # 查找观点对立的宠物
        query = """
        MATCH (p1:Pet)
        MATCH (p2:Pet)
        WHERE p1.pet_id IN $user_pets 
          AND p2.pet_id IN $user_pets
          AND (p1)-[:OPPOSITE_TO]-(p2)
        RETURN p1, p2, 
            CASE 
                WHEN $topic = 'risk' THEN p1.risk_tolerance <> p2.risk_tolerance
                WHEN $topic = 'style' THEN p1.investment_style <> p2.investment_style
                ELSE false
            END AS is_relevant
        ORDER BY is_relevant DESC
        LIMIT 1
        """
        
        result = self.db.run(query, user_pets=user_pets, topic=topic)
        
        if result:
            record = result[0]
            return {
                'pet_a': record['p1'],
                'pet_b': record['p2'],
                'debate_topic': topic
            }
        
        return None
```

### 5.3 宠物协作场景

```python
class PetCollaboration:
    def __init__(self, graph_db):
        self.db = graph_db
    
    def select_collaborators(self, task_type, user_pets):
        """为任务类型选择协作宠物"""
        
        # 查找专长互补的宠物
        query = """
        MATCH (p1:Pet)
        MATCH (p2:Pet)
        WHERE p1.pet_id IN $user_pets 
          AND p2.pet_id IN $user_pets
          AND (p1)-[:COLLABORATES_WITH]-(p2)
          AND $task_type IN p1.expertise
          AND $task_type IN p2.expertise
        RETURN p1, p2, 
            (p1.proactivity_level + p2.proactivity_level) / 2 AS avg_proactivity
        ORDER BY avg_proactivity DESC
        LIMIT 1
        """
        
        result = self.db.run(query, user_pets=user_pets, task_type=task_type)
        
        if result:
            record = result[0]
            return {
                'pet_a': record['p1'],
                'pet_b': record['p2'],
                'collaboration_type': task_type
            }
        
        return None
```

---

## 六、图可视化组件

### 6.1 React 组件

```jsx
// PetRelationGraph.jsx
import React, { useEffect, useRef, useState } from 'react';
import * as echarts from 'echarts';

const PetRelationGraph = ({ userId, initialPet }) => {
    const chartRef = useRef(null);
    const [graphData, setGraphData] = useState(null);
    const [selectedPet, setSelectedPet] = useState(null);

    useEffect(() => {
        // 加载图谱数据
        loadGraphData(userId, initialPet);
    }, [userId, initialPet]);

    useEffect(() => {
        if (graphData && chartRef.current) {
            initChart(graphData);
        }
    }, [graphData]);

    const loadGraphData = async (userId, initialPet) => {
        const response = await fetch(`/api/graph/pets?user_id=${userId}&center=${initialPet}`);
        const data = await response.json();
        setGraphData(data);
    };

    const initChart = (data) => {
        const chart = echarts.init(chartRef.current);
        
        const option = {
            tooltip: {
                formatter: (x) => formatTooltip(x.data)
            },
            series: [{
                type: 'graph',
                layout: 'force',
                data: data.nodes,
                links: data.links,
                categories: data.categories,
                roam: true,
                label: { show: true, position: 'right' },
                force: {
                    repulsion: 300,
                    edgeLength: [100, 300],
                    gravity: 0.1
                },
                lineStyle: {
                    color: 'source',
                    curveness: 0.3
                },
                emphasis: {
                    focus: 'adjacency'
                }
            }]
        };

        chart.setOption(option);

        // 点击事件
        chart.on('click', (params) => {
            if (params.dataType === 'node') {
                setSelectedPet(params.data);
            }
        });
    };

    return (
        <div className="pet-relation-graph">
            <div ref={chartRef} style={{ width: '100%', height: '600px' }} />
            {selectedPet && (
                <PetDetailPanel pet={selectedPet} />
            )}
        </div>
    );
};

export default PetRelationGraph;
```

### 6.2 宠物详情面板

```jsx
// PetDetailPanel.jsx
const PetDetailPanel = ({ pet }) => {
    return (
        <div className="pet-detail-panel">
            <h3>{pet.name}</h3>
            <img src={pet.avatar_url} alt={pet.name} />
            
            <div className="pet-stats">
                <div>投资风格：{pet.investment_style}</div>
                <div>风险偏好：{pet.risk_tolerance}</div>
                <div>主动性：{pet.proactivity_level}</div>
                <div>干预阈值：{pet.intervention_threshold}</div>
            </div>

            <div className="pet-relationships">
                <h4>关系网络</h4>
                <ul>
                    {pet.relationships.map(rel => (
                        <li key={rel.target_id}>
                            {rel.type}: {rel.target_name}
                        </li>
                    ))}
                </ul>
            </div>

            <button onClick={() => selectAsMainPet(pet.pet_id)}>
                设为主宠物
            </button>
        </div>
    );
};
```

---

## 七、API 接口设计

### 7.1 图查询 API

```python
# routes/graph.py
from fastapi import APIRouter, Query
from typing import List, Optional

router = APIRouter(prefix="/api/graph", tags=["graph"])

@router.get("/pets")
async def get_pet_graph(
    user_id: str = Query(...),
    center: Optional[str] = Query(None),
    depth: int = Query(2, ge=1, le=5)
):
    """获取宠物关系图谱"""
    
    if center:
        # 以指定宠物为中心
        query = """
        MATCH (center:Pet {pet_id: $center})
        MATCH path = (center)-[*1..$depth]-(other:Pet)
        RETURN path
        """
    else:
        # 完整图谱
        query = """
        MATCH (p:Pet)
        MATCH (p)-[r]-(other:Pet)
        RETURN p, r, other
        """
    
    result = db.run(query, center=center, depth=depth)
    
    return format_graph_result(result)

@router.get("/pets/{pet_id}/compatible")
async def get_compatible_pets(pet_id: str, min_strength: float = 0.5):
    """获取兼容宠物"""
    
    query = """
    MATCH (p:Pet {pet_id: $pet_id})-[r:COMPATIBLE_WITH]->(other:Pet)
    WHERE r.strength >= $min_strength
    RETURN other, r.strength
    ORDER BY r.strength DESC
    """
    
    result = db.run(query, pet_id=pet_id, min_strength=min_strength)
    
    return [
        {
            'pet_id': record['other']['pet_id'],
            'name': record['other']['name'],
            'strength': record['r.strength']
        }
        for record in result
    ]

@router.get("/pets/{pet_id}/path/{target_pet_id}")
async def get_pet_path(pet_id: str, target_pet_id: str):
    """获取两只宠物之间的关系路径"""
    
    query = """
    MATCH path = shortestPath(
        (p1:Pet {pet_id: $pet_id})-[*1..5]-(p2:Pet {pet_id: $target_pet_id})
    )
    RETURN path
    """
    
    result = db.run(query, pet_id=pet_id, target_pet_id=target_pet_id)
    
    if result:
        return format_path_result(result[0]['path'])
    
    return {'error': 'No path found'}

@router.post("/pets/recommend")
async def recommend_pets(user_profile: UserProfile, top_k: int = 3):
    """推荐宠物"""
    
    # 基于用户性格匹配
    query = """
    MATCH (p:Pet)
    WHERE 
        (p.investment_style = $invest_style) OR
        (p.risk_tolerance = $risk_tol)
    WITH p, 
        CASE WHEN p.investment_style = $invest_style THEN 0.6 ELSE 0 END +
        CASE WHEN p.risk_tolerance = $risk_tol THEN 0.4 ELSE 0 END 
        AS score
    RETURN p, score
    ORDER BY score DESC
    LIMIT $top_k
    """
    
    result = db.run(query, 
        invest_style=user_profile.investment_style,
        risk_tol=user_profile.risk_tolerance,
        top_k=top_k
    )
    
    return [format_pet_result(record['p']) for record in result]
```

---

## 八、MVP 范围

### 8.1 MVP 功能（P0）

| 功能 | 说明 | 优先级 |
|------|------|--------|
| Neo4j 图数据库 | 存储宠物关系 | P0 |
| 基础关系图 | ECharts 可视化 | P0 |
| 宠物节点 | 12 只宠物基础信息 | P0 |
| 关系边 | 兼容/对立关系 | P0 |

### 8.2 首期迭代（P1）

| 功能 | 说明 | 优先级 |
|------|------|--------|
| 用户 - 宠物关系 | 拥有/互动关系 | P1 |
| 图查询 API | RESTful 接口 | P1 |
| 交互功能 | 点击/拖拽/缩放 | P1 |
| 宠物推荐 | 基于性格匹配 | P1 |

### 8.3 后续版本（P2）

| 功能 | 说明 | 优先级 |
|------|------|--------|
| 动态演化 | 关系随互动变化 | P2 |
| 社区发现 | Louvain 算法 | P2 |
| 宠物辩论 | 自动选择对立宠物 | P2 |
| 3D 可视化 | 3D 力导向布局 | P2 |

---

## 九、数据表设计（关系型备份）

### 9.1 宠物关系表

```sql
CREATE TABLE pet_relationships (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    from_pet_id VARCHAR(32) NOT NULL COMMENT '源宠物 ID',
    to_pet_id VARCHAR(32) NOT NULL COMMENT '目标宠物 ID',
    relationship_type VARCHAR(32) NOT NULL COMMENT '关系类型',
    strength DECIMAL(3,2) DEFAULT 0.5 COMMENT '关系强度',
    properties JSON COMMENT '关系属性',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE KEY uk_from_to_type (from_pet_id, to_pet_id, relationship_type),
    INDEX idx_from_pet (from_pet_id),
    INDEX idx_to_pet (to_pet_id),
    FOREIGN KEY (from_pet_id) REFERENCES pets(pet_id),
    FOREIGN KEY (to_pet_id) REFERENCES pets(pet_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='宠物关系表';
```

### 9.2 用户宠物关系表

```sql
CREATE TABLE user_pet_relationships (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id VARCHAR(64) NOT NULL COMMENT '用户 ID',
    pet_id VARCHAR(32) NOT NULL COMMENT '宠物 ID',
    relationship_type VARCHAR(32) DEFAULT 'owns' COMMENT '关系类型',
    intimacy INT DEFAULT 0 COMMENT '亲密度',
    interaction_count BIGINT DEFAULT 0 COMMENT '互动次数',
    last_interaction_at TIMESTAMP NULL COMMENT '最后互动时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY uk_user_pet (user_id, pet_id),
    INDEX idx_user (user_id),
    INDEX idx_pet (pet_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户宠物关系表';
```

---

*最后更新：2026-04-11 | Day 1/10 完成度 80%*
