from mragent.agent_workflow import MRAgent
import pandas as pd
import os

class MRAgentOE(MRAgent):
    def __init__(self, mode='OE', exposure=None, outcome=None, AI_key=None, model='MR', num=100, bidirectional=False,
                 synonyms=True, introduction=True, LLM_model='gpt-4o', model_type='openai', base_url=None,
                 gwas_token=None,
                 opengwas_mode='online', gwas_source='opengwas', mr_quality_evaluation=False, mr_quality_evaluation_key_item=None, mrlap=False):
        super().__init__(mode, exposure=exposure, outcome=outcome, AI_key=AI_key, model=model, num=num,
                         bidirectional=bidirectional, synonyms=synonyms, introduction=introduction,
                         LLM_model=LLM_model, model_type=model_type, base_url=base_url, gwas_token=gwas_token,
                         opengwas_mode=opengwas_mode, gwas_source=gwas_source,
                         mr_quality_evaluation=mr_quality_evaluation,
                         mr_quality_evaluation_key_item=mr_quality_evaluation_key_item, mrlap=mrlap)

    def step1(self):
        print(self.path)
        # 新建一个df然后保存到Exposure_and_Outcome.csv
        # 创建一个带有数据的DataFrame
        data = {'index': [1], 'Outcome': [self.outcome], 'Exposure': [self.exposure], 'title': ['title null'],
                'oeID': [1]}
        df = pd.DataFrame(data)
        df.to_csv(os.path.join(self.path, 'Exposure_and_Outcome.csv'), index=False)  # 保存到csv文件

        # 打印DataFrame
        print(df)
