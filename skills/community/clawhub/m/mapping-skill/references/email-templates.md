# Email Templates Library (邮件模板库)

本文档包含 22 个研究领域的个性化邮件模板，用于与 AI/ML 研究人员进行初次联系。

## 使用方法

1. **确定候选人领域**: 使用 `field-mappings.md` 确定候选人的标准化研究领域
2. **选择对应模板**: 使用候选人的研究领域获取对应的邮件模板
3. **填充占位符**: 将模板中的占位符替换为实际内容
4. **融入话术**: 从 `talk-tracks.md` 中选择相关话术填充 `{{talk_track_paragraph}}`

## 模板占位符说明

| 占位符 | 说明 | 示例 |
|--------|------|------|
| `{{researcher_name}}` | 候选人姓名 | Wei Zhang |
| `{{context_affiliation}}` | 候选人所属机构 | Tsinghua University |
| `{{research_field}}` | 候选人研究方向 | Reinforcement Learning |
| `{{technical_hook}}` | **核心**: 与候选人研究相关的技术连接点 | 特别是在sparse attention机制优化训练效率方面 |
| `{{talk_track_paragraph}}` | **核心**: 展示领域深度的 3-4 句话 | 基于talk-tracks.md生成的段落 |

---

## 邮件模板结构

所有模板遵循以下结构：

```
Hi, {{researcher_name}},

我是Mark，陆奇博士的奇绩创坛研究团队Member。

[领域特定开场白] 最近关注到你在{{context_affiliation}}做的关于{{research_field}}方向的研究。
我们对于[领域描述]非常关注，特别是在{{technical_hook}}方面有非常大的兴趣。

{{talk_track_paragraph}}

希望引荐陆奇博士研究团队Team Lead Jack Jin与你认识交流～他对GenAI时代的模型架构、理论、Infra都有着很深的思考！
一方面想了解一下你最近研究和工作上的Curiosity，做一些技术/Research交流，另一方面如果有好的早期机会也可以介绍给你。
同时我们也在建立面向华人学者的社区，主要是帮你在未来链接到好的资源。

希望在微信上帮你和Jack拉一个群，交流技术与长期合作机会，可以扫一下我的微信。（抱歉用个人邮箱，奇绩创坛有时候被弹回）
微信号：foundersfirst27

奇绩创坛
Mark
```

---

## 1. RL (强化学习)

```
Hi, {{researcher_name}},

我是Mark，陆奇博士的奇绩创坛研究团队Member。

作为持续关注决策智能发展的研究者，我注意到您在{{context_affiliation}}关于{{research_field}}方向的探索。
我们团队对强化学习如何驱动更优的长期策略非常感兴趣，尤其关注到{{technical_hook}}。

{{talk_track_paragraph}}

希望引荐陆奇博士研究团队Team Lead Jack Jin与你认识交流～他对GenAI时代的模型架构、理论、Infra都有着很深的思考！
一方面想了解一下你最近研究和工作上的Curiosity，做一些技术/Research交流，另一方面如果有好的早期机会也可以介绍给你。
同时我们也在建立面向华人学者的社区，主要是帮你在未来链接到好的资源。

希望在微信上帮你和Jack拉一个群，交流技术与长期合作机会，可以扫一下我的微信。（抱歉用个人邮箱，奇绩创坛有时候被弹回）
微信号：foundersfirst27

奇绩创坛
Mark
```

---

## 2. Pre/Post-train × RL (模型自我进化)

```
Hi, {{researcher_name}},

我是Mark，陆奇博士的奇绩创坛研究团队Member。

在模型自我进化与闭环训练的前沿领域，我关注到您在{{context_affiliation}}关于{{research_field}}方向的研究。
我们对{{technical_hook}}等突破性工作非常感兴趣，这正在重新定义模型训练的范式。

{{talk_track_paragraph}}

希望引荐陆奇博士研究团队Team Lead Jack Jin与你认识交流～他对GenAI时代的模型架构、理论、Infra都有着很深的思考！
一方面想了解一下你最近研究和工作上的Curiosity，做一些技术/Research交流，另一方面如果有好的早期机会也可以介绍给你。
同时我们也在建立面向华人学者的社区，主要是帮你在未来链接到好的资源。

希望在微信上帮你和Jack拉一个群，交流技术与长期合作机会，可以扫一下我的微信。（抱歉用个人邮箱，奇绩创坛有时候被弹回）
微信号：foundersfirst27

奇绩创坛
Mark
```

---

## 3. NLP (自然语言处理)

```
Hi, {{researcher_name}},

我是Mark，陆奇博士的奇绩创坛研究团队Member。

作为一名NLP领域的从业者，我最近学习了您在{{context_affiliation}}关于{{research_field}}方面的研究，深受启发。
您对于语言模型的深刻理解和创新应用，正是我们当前非常关注的，特别是在{{technical_hook}}方面。

{{talk_track_paragraph}}

希望引荐陆奇博士研究团队Team Lead Jack Jin与你认识交流～他对GenAI时代的模型架构、理论、Infra都有着很深的思考！
一方面想了解一下你最近研究和工作上的Curiosity，做一些技术/Research交流，另一方面如果有好的早期机会也可以介绍给你。
同时我们也在建立面向华人学者的社区，主要是帮你在未来链接到好的资源。

希望在微信上帮你和Jack拉一个群，交流技术与长期合作机会，可以扫一下我的微信。（抱歉用个人邮箱，奇绩邮箱有时候被弹回）
微信号：foundersfirst27

奇绩创坛
Mark
```

---

## 4. MOE (混合专家)

```
Hi, {{researcher_name}},

我是Mark，陆奇博士的奇绩创坛研究团队Member。

混合专家模型架构正在重塑大模型的效率边界。关注到您在{{context_affiliation}}关于{{research_field}}方向的研究，
我们对您在{{technical_hook}}方面的创新非常感兴趣，这将决定下一代模型架构的演进方向。

{{talk_track_paragraph}}

希望引荐陆奇博士研究团队Team Lead Jack Jin与你认识交流～他对GenAI时代的模型架构、理论、Infra都有着很深的思考！
一方面想了解一下你最近研究和工作上的Curiosity，做一些技术/Research交流，另一方面如果有好的早期机会也可以介绍给你。
同时我们也在建立面向华人学者的社区，主要是帮你在未来链接到好的资源。

希望在微信上帮你和Jack拉一个群，交流技术与长期合作机会，可以扫一下我的微信。（抱歉用个人邮箱，奇绩创坛有时候被弹回）
微信号：foundersfirst27

奇绩创坛
Mark
```

---

## 5. EVAL (评估)

```
Hi, {{researcher_name}},

我是Mark，陆奇博士的奇绩创坛研究团队Member。

模型评估是AI发展的关键标尺。看到您在{{context_affiliation}}关于{{research_field}}方向的工作，
我们对您在{{technical_hook}}方面的研究方法印象深刻，这对于客观衡量和推动AI进步至关重要。

{{talk_track_paragraph}}

希望引荐陆奇博士研究团队Team Lead Jack Jin与你认识交流～他对GenAI时代的模型架构、理论、Infra都有着很深的思考！
一方面想了解一下你最近研究和工作上的Curiosity，做一些技术/Research交流，另一方面如果有好的早期机会也可以介绍给你。
同时我们也在建立面向华人学者的社区，主要是帮你在未来链接到好的资源。

希望在微信上帮你和Jack拉一个群，交流技术与长期合作机会，可以扫一下我的微信。（抱歉用个人邮箱，奇绩创坛有时候被弹回）
微信号：foundersfirst27

奇绩创坛
Mark
```

---

## 6. data (数据)

```
Hi, {{researcher_name}},

我是Mark，陆奇博士的奇绩创坛研究团队Member。

数据是驱动现代AI模型能力的核心燃料。看到您在{{context_affiliation}}关于{{research_field}}方向的工作，
我们对您在{{technical_hook}}方面的见解和方法印象深刻，并认为这对于构筑更高质量的数据壁垒至关重要。

{{talk_track_paragraph}}

希望引荐陆奇博士研究团队Team Lead Jack Jin与你认识交流～他对GenAI时代的模型架构、理论、Infra都有着很深的思考！
一方面想了解一下你最近研究和工作上的Curiosity，做一些技术/Research交流，另一方面如果有好的早期机会也可以介绍给你。
同时我们也在建立面向华人学者的社区，主要是帮你在未来链接到好的资源。

希望在微信上帮你和Jack拉一个群，交流技术与长期合作机会，可以扫一下我的微信。（抱歉用个人邮箱，奇绩创坛有时候被弹回）
微信号：foundersfirst27

奇绩创坛
Mark
```

---

## 7. AI4S (AI for Science)

```
Hi, {{researcher_name}},

我是Mark，陆奇博士的奇绩创坛研究团队Member。

AI for Science 正在加速基础科学的发现范式。关注到您在{{context_affiliation}}将AI应用于{{research_field}}领域的工作，
我们认为您在{{technical_hook}}方面的研究，对于推动科学边界有重要意义。

{{talk_track_paragraph}}

希望引荐陆奇博士研究团队Team Lead Jack Jin与你认识交流～他对GenAI时代的模型架构、理论、Infra都有着很深的思考！
一方面想了解一下你最近研究和工作上的Curiosity，做一些技术/Research交流，另一方面如果有好的早期机会也可以介绍给你。
同时我们也在建立面向华人学者的社区，主要是帮你在未来链接到好的资源。

希望在微信上帮你和Jack拉一个群，交流技术与长期合作机会，可以扫一下我的微信。（抱歉用个人邮箱，奇绩创坛有时候被弹回）
微信号：foundersfirst27

奇绩创坛
Mark
```

---

## 8. Audio (语音)

```
Hi, {{researcher_name}},

我是Mark，陆奇博士的奇绩创坛研究团队Member。

在语音交互日益成为主流的今天，我们关注到您在{{context_affiliation}}关于{{research_field}}方向的深入研究。
我们对于{{technical_hook}}等下一代语音技术非常感兴趣。

{{talk_track_paragraph}}

希望引荐陆奇博士研究团队Team Lead Jack Jin与你认识交流～他对GenAI时代的模型架构、理论、Infra都有着很深的思考！
一方面想了解一下你最近研究和工作上的Curiosity，做一些技术/Research交流，另一方面如果有好的早期机会也可以介绍给你。
同时我们也在建立面向华人学者的社区，主要是帮你在未来链接到好的资源。

希望在微信上帮你和Jack拉一个群，交流技术与长期合作机会，可以扫一下我的微信。（抱歉用个人邮箱，奇绩创坛有时候被弹回）
微信号：foundersfirst27

奇绩创坛
Mark
```

---

## 9. MLSys (机器学习系统)

```
Hi, {{researcher_name}},

我是Mark，陆奇博士的奇绩创坛研究团队Member。

我们深知系统工程是释放AI潜能的关键。了解到您在{{context_affiliation}}关于{{research_field}}方向的研究，
我们对您在{{technical_hook}}方面的思考和实践印象深刻。

{{talk_track_paragraph}}

希望引荐陆奇博士研究团队Team Lead Jack Jin与你认识交流～他对GenAI时代的模型架构、理论、Infra都有着很深的思考！
一方面想了解一下你最近研究和工作上的Curiosity，做一些技术/Research交流，另一方面如果有好的早期机会也可以介绍给你。
同时我们也在建立面向华人学者的社区，主要是帮你在未来链接到好的资源。

希望在微信上帮你和Jack拉一个群，交流技术与长期合作机会，可以扫一下我的微信。（抱歉用个人邮箱，奇绩创坛有时候被弹回）
微信号：foundersfirst27

奇绩创坛
Mark
```

---

## 10. LLM4CODE (代码生成)

```
Hi, {{researcher_name}},

我是Mark，陆奇博士的奇绩创坛研究团队Member。

代码是数字世界的通用语言，而LLM正在重塑软件开发的未来。关注到您在{{context_affiliation}}关于{{research_field}}方向的研究，
我们对您在{{technical_hook}}方面的探索非常感兴趣。

{{talk_track_paragraph}}

希望引荐陆奇博士研究团队Team Lead Jack Jin与你认识交流～他对GenAI时代的模型架构、理论、Infra都有着很深的思考！
一方面想了解一下你最近研究和工作上的Curiosity，做一些技术/Research交流，另一方面如果有好的早期机会也可以介绍给你。
同时我们也在建立面向华人学者的社区，主要是帮你在未来链接到好的资源。

希望在微信上帮你和Jack拉一个群，交流技术与长期合作机会，可以扫一下我的微信。（抱歉用个人邮箱，奇绩创坛有时候被弹回）
微信号：foundersfirst27

奇绩创坛
Mark
```

---

## 11. Multimodal (多模态)

```
Hi, {{researcher_name}},

我是Mark，陆奇博士的奇绩创坛研究团队Member。

在多模态技术正融合语言、视觉及更多感官信息的当下，我关注到您在{{context_affiliation}}做的关于{{research_field}}方向的研究。
我们对{{technical_hook}}等如何构建更全面的世界理解非常感兴趣。

{{talk_track_paragraph}}

希望引荐陆奇博士研究团队Team Lead Jack Jin与你认识交流～他对GenAI时代的模型架构、理论、Infra都有着很深的思考！
一方面想了解一下你最近研究和工作上的Curiosity，做一些技术/Research交流，另一方面如果有好的早期机会也可以介绍给你。
同时我们也在建立面向华人学者的社区，主要是帮你在未来链接到好的资源。

希望在微信上帮你和Jack拉一个群，交流技术与长期合作机会，可以扫一下我的微信。（抱歉用个人邮箱，奇绩创坛有时候被弹回）
微信号：foundersfirst27

奇绩创坛
Mark
```

---

## 12. Pre-training (预训练)

```
Hi, {{researcher_name}},

我是Mark，陆奇博士的奇绩创坛研究团队Member。

预训练是构筑AI能力基础的黄金阶段。看到您在{{context_affiliation}}关于{{research_field}}方向的研究，
我们对您在{{technical_hook}}方面的探索印象深刻，这将决定下一代基础模型的能力上限。

{{talk_track_paragraph}}

希望引荐陆奇博士研究团队Team Lead Jack Jin与你认识交流～他对GenAI时代的模型架构、理论、Infra都有着很深的思考！
一方面想了解一下你最近研究和工作上的Curiosity，做一些技术/Research交流，另一方面如果有好的早期机会也可以介绍给你。
同时我们也在建立面向华人学者的社区，主要是帮你在未来链接到好的资源。

希望在微信上帮你和Jack拉一个群，交流技术与长期合作机会，可以扫一下我的微信。（抱歉用个人邮箱，奇绩创坛有时候被弹回）
微信号：foundersfirst27

奇绩创坛
Mark
```

---

## 13. post-train (后训练)

```
Hi, {{researcher_name}},

我是Mark，陆奇博士的奇绩创坛研究团队Member。

后训练是将基础模型转化为实用工具的关键环节。关注到您在{{context_affiliation}}关于{{research_field}}方向的研究，
我们对您在{{technical_hook}}方面的创新方法非常感兴趣，这正在重新定义模型微调的效率边界。

{{talk_track_paragraph}}

希望引荐陆奇博士研究团队Team Lead Jack Jin与你认识交流～他对GenAI时代的模型架构、理论、Infra都有着很深的思考！
一方面想了解一下你最近研究和工作上的Curiosity，做一些技术/Research交流，另一方面如果有好的早期机会也可以介绍给你。
同时我们也在建立面向华人学者的社区，主要是帮你在未来链接到好的资源。

希望在微信上帮你和Jack拉一个群，交流技术与长期合作机会，可以扫一下我的微信。（抱歉用个人邮箱，奇绩创坛有时候被弹回）
微信号：foundersfirst27

奇绩创坛
Mark
```

---

## 14. Alignment (对齐)

```
Hi, {{researcher_name}},

我是Mark，陆奇博士的奇绩创坛研究团队Member。

模型对齐是确保AI安全可控的关键保障。看到您在{{context_affiliation}}关于{{research_field}}方向的研究，
我们对您在{{technical_hook}}方面的工作深感敬佩，这正在为超级对齐的实现奠定重要基础。

{{talk_track_paragraph}}

希望引荐陆奇博士研究团队Team Lead Jack Jin与你认识交流～他对GenAI时代的模型架构、理论、Infra都有着很深的思考！
一方面想了解一下你最近研究和工作上的Curiosity，做一些技术/Research交流，另一方面如果有好的早期机会也可以介绍给你。
同时我们也在建立面向华人学者的社区，主要是帮你在未来链接到好的资源。

希望在微信上帮你和Jack拉一个群，交流技术与长期合作机会，可以扫一下我的微信。（抱歉用个人邮箱，奇绩创坛有时候被弹回）
微信号：foundersfirst27

奇绩创坛
Mark
```

---

## 15. Reasoning (推理)

```
Hi, {{researcher_name}},

我是Mark，陆奇博士的奇绩创坛研究团队Member。

推理（Reasoning）是通向通用人工智能的基石。最近关注到您在{{context_affiliation}}关于{{research_field}}方向的杰出工作，
我们对如何提升模型的复杂推理能力，尤其是在{{technical_hook}}方面，有非常大的兴趣。

{{talk_track_paragraph}}

希望引荐陆奇博士研究团队Team Lead Jack Jin与你认识交流～他对GenAI时代的模型架构、理论、Infra都有着很深的思考！
一方面想了解一下你最近研究和工作上的Curiosity，做一些技术/Research交流，另一方面如果有好的早期机会也可以介绍给你。
同时我们也在建立面向华人学者的社区，主要是帮你在未来链接到好的资源。

希望在微信上帮你和Jack拉一个群，交流技术与长期合作机会，可以扫一下我的微信。（抱歉用个人邮箱，奇绩创坛有时候被弹回）
微信号：foundersfirst27

奇绩创坛
Mark
```

---

## 16. Agent&RAG (智能体与检索)

```
Hi, {{researcher_name}},

我是Mark，陆奇博士的奇绩创坛研究团队Member。

随着智能体（Agent）和RAG技术重新定义人机交互的边界，我们注意到您在{{context_affiliation}}关于{{research_field}}方向的工作。
我们对如何构建更强大的Agent能力非常关注，特别是{{technical_hook}}方面。

{{talk_track_paragraph}}

希望引荐陆奇博士研究团队Team Lead Jack Jin与你认识交流～他对GenAI时代的模型架构、理论、Infra都有着很深的思考！
一方面想了解一下你最近研究和工作上的Curiosity，做一些技术/Research交流，另一方面如果有好的早期机会也可以介绍给你。
同时我们也在建立面向华人学者的社区，主要是帮你在未来链接到好的资源。

希望在微信上帮你和Jack拉一个群，交流技术与长期合作机会，可以扫一下我的微信。（抱歉用个人邮箱，奇绩创坛有时候被弹回）
微信号：foundersfirst27

奇绩创坛
Mark
```

---

## 17. Interpretable AI (可解释AI)

```
Hi, {{researcher_name}},

我是Mark，陆奇博士的奇绩创坛研究团队Member。

可解释AI是理解智能本质的重要窗口。关注到您在{{context_affiliation}}关于{{research_field}}方向的研究，
我们对您在{{technical_hook}}方面的探索非常感兴趣，这将帮助揭开AI模型的"黑箱"之谜。

{{talk_track_paragraph}}

希望引荐陆奇博士研究团队Team Lead Jack Jin与你认识交流～他对GenAI时代的模型架构、理论、Infra都有着很深的思考！
一方面想了解一下你最近研究和工作上的Curiosity，做一些技术/Research交流，另一方面如果有好的早期机会也可以介绍给你。
同时我们也在建立面向华人学者的社区，主要是帮你在未来链接到好的资源。

希望在微信上帮你和Jack拉一个群，交流技术与长期合作机会，可以扫一下我的微信。（抱歉用个人邮箱，奇绩创坛有时候被弹回）
微信号：foundersfirst27

奇绩创坛
Mark
```

---

## 18. Embodiment (具身智能)

```
Hi, {{researcher_name}},

我是Mark，陆奇博士的奇绩创坛研究团队Member。

我们相信具身智能是AI与物理世界交互的终极形态。看到您在{{context_affiliation}}关于{{research_field}}方面的研究工作，
我们对您在{{technical_hook}}的探索印象深刻，并认为这对于构建真正自主的智能体至关重要。

{{talk_track_paragraph}}

希望引荐陆奇博士研究团队Team Lead Jack Jin与你认识交流～他对GenAI时代的模型架构、理论、Infra都有着很深的思考！
一方面想了解一下你最近研究和工作上的Curiosity，做一些技术/Research交流，另一方面如果有好的早期机会也可以介绍给你。
同时我们也在建立面向华人学者的社区，主要是帮你在未来链接到好的资源。

希望在微信上帮你和Jack拉一个群，交流技术与长期合作机会，可以扫一下我的微信。（抱歉用个人邮箱，奇绩创坛有时候被弹回）
微信号：foundersfirst27

奇绩创坛
Mark
```

---

## 19. Computer Vision (计算机视觉)

```
Hi, {{researcher_name}},

我是Mark，陆奇博士的奇绩创坛研究团队Member。

作为计算机视觉领域的同行，我十分钦佩您在{{context_affiliation}}关于{{research_field}}方向上的建树。
您的研究对于解决真实世界的视觉问题具有很高的价值，我们尤其对您在{{technical_hook}}方面的思路非常感兴趣。

{{talk_track_paragraph}}

希望引荐陆奇博士研究团队Team Lead Jack Jin与你认识交流～他对GenAI时代的模型架构、理论、Infra都有着很深的思考！
一方面想了解一下你最近研究和工作上的Curiosity，做一些技术/Research交流，另一方面如果有好的早期机会也可以介绍给你。
同时我们也在建立面向华人学者的社区，主要是帮你在未来链接到好的资源。

希望在微信上帮你和Jack拉一个群，交流技术与长期合作机会，可以扫一下我的微信。（抱歉用个人邮箱，奇绩邮箱有时候被弹回）
微信号：foundersfirst27

奇绩创坛
Mark
```

---

## 20. Recommendation System (推荐系统)

```
Hi, {{researcher_name}},

我是Mark，陆奇博士的奇绩创坛研究团队Member。

推荐系统正在被LLM技术重新定义。看到您在{{context_affiliation}}关于{{research_field}}方向的研究，
我们对您在{{technical_hook}}方面的创新印象深刻，这将为个性化服务带来全新可能。

{{talk_track_paragraph}}

希望引荐陆奇博士研究团队Team Lead Jack Jin与你认识交流～他对GenAI时代的模型架构、理论、Infra都有着很深的思考！
一方面想了解一下你最近研究和工作上的Curiosity，做一些技术/Research交流，另一方面如果有好的早期机会也可以介绍给你。
同时我们也在建立面向华人学者的社区，主要是帮你在未来链接到好的资源。

希望在微信上帮你和Jack拉一个群，交流技术与长期合作机会，可以扫一下我的微信。（抱歉用个人邮箱，奇绩创坛有时候被弹回）
微信号：foundersfirst27

奇绩创坛
Mark
```

---

## 21. Federated Learning (联邦学习)

```
Hi, {{researcher_name}},

我是Mark，陆奇博士的奇绩创坛研究团队Member。

联邦学习正在重塑数据隐私与模型训练的平衡。关注到您在{{context_affiliation}}关于{{research_field}}方向的研究，
我们对您在{{technical_hook}}方面的突破性工作非常感兴趣，这将推动分布式AI的安全发展。

{{talk_track_paragraph}}

希望引荐陆奇博士研究团队Team Lead Jack Jin与你认识交流～他对GenAI时代的模型架构、理论、Infra都有着很深的思考！
一方面想了解一下你最近研究和工作上的Curiosity，做一些技术/Research交流，另一方面如果有好的早期机会也可以介绍给你。
同时我们也在建立面向华人学者的社区，主要是帮你在未来链接到好的资源。

希望在微信上帮你和Jack拉一个群，交流技术与长期合作机会，可以扫一下我的微信。（抱歉用个人邮箱，奇绩创坛有时候被弹回）
微信号：foundersfirst27

奇绩创坛
Mark
```

---

## 22. Trustworthy AI (可信AI)

```
Hi, {{researcher_name}},

我是Mark，陆奇博士的奇绩创坛研究团队Member。

可信AI是技术落地的安全基石。看到您在{{context_affiliation}}关于{{research_field}}方向的工作，
我们对您在{{technical_hook}}方面的研究深感敬佩，这正在为AI的可靠性和鲁棒性树立新标准。

{{talk_track_paragraph}}

希望引荐陆奇博士研究团队Team Lead Jack Jin与你认识交流～他对GenAI时代的模型架构、理论、Infra都有着很深的思考！
一方面想了解一下你最近研究和工作上的Curiosity，做一些技术/Research交流，另一方面如果有好的早期机会也可以介绍给你。
同时我们也在建立面向华人学者的社区，主要是帮你在未来链接到好的资源。

希望在微信上帮你和Jack拉一个群，交流技术与长期合作机会，可以扫一下我的微信。（抱歉用个人邮箱，奇绩创坛有时候被弹回）
微信号：foundersfirst27

奇绩创坛
Mark
```

---

## Default (默认模板)

如果没有匹配到具体领域，使用以下通用模板：

```
Hi, {{researcher_name}},

我是Mark，陆奇博士的奇绩创坛研究团队Member。

最近关注到你在{{context_affiliation}}做的关于{{research_field}}方向的研究。
我们对于前沿AI领域非常关注，特别是在{{technical_hook}}方面有非常大的兴趣。

{{talk_track_paragraph}}

希望引荐陆奇博士研究团队Team Lead Jack Jin与你认识交流～他对GenAI时代的模型架构、理论、Infra都有着很深的思考！
一方面想了解一下你最近研究和工作上的Curiosity，做一些技术/Research交流，另一方面如果有好的早期机会也可以介绍给你。
同时我们也在建立面向华人学者的社区，主要是帮你在未来链接到好的资源。

希望在微信上帮你和Jack拉一个群，交流技术与长期合作机会，可以扫一下我的微信。（抱歉用个人邮箱，奇绩创坛有时候被弹回）
微信号：foundersfirst27

奇绩创坛
Mark
```
