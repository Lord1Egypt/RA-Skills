# clawhub

#### Description
聚宽(JoinQuant)策略回测代码生成框架 - 六段式骨架模板+多因子选股+时序择时，使用聚宽原生API获取数据

#### Software Architecture
Hermes Agent Skill architecture: SKILL.md (main) + references/ + templates/

#### Installation

1.  Clone this repo
2.  Copy `SKILL.md` to your Hermes Agent skills directory
3.  Copy `references/` and `templates/` alongside it

#### Instructions

1.  Load the skill in Hermes Agent
2.  Describe your strategy requirements (factors / targets / parameters)
3.  Agent selects template, fills in parameters, generates complete code
4.  Copy generated code to JoinQuant platform and run backtest

#### Factor IC Lookup

Visit JoinQuant factor library: https://www.joinquant.com/view/factorlib/list

#### Contribution

1.  Fork the repository
2.  Create Feat_xxx branch
3.  Commit your code
4.  Create Pull Request
