import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from data_manager import DataManager
from inventory import InventoryManager
from demand_calculator import DemandCalculator
from anomaly_detector import AnomalyDetector
from predictor import DemandPredictor
from datetime import datetime

class SparePartsSystem:
    def __init__(self, excel_path='data/spare_parts.xlsx'):
        self.dm = DataManager(excel_path)
        self.im = InventoryManager(self.dm)
        self.dc = DemandCalculator(self.dm)
        self.ad = AnomalyDetector(self.dm)
        self.dp = DemandPredictor(self.dm)
    
    def query_inventory(self, part_id=None):
        if part_id:
            return self.im.query_inventory(part_id)
        return self.im.query_all_inventory()
    
    def calculate_demand(self, part_id=None, days=30):
        if part_id:
            return self.dc.calculate_demand(part_id, days)
        return self.dc.calculate_all_demands(days)
    
    def calculate_replenishment(self, part_id=None, days=30):
        if part_id:
            return self.dc.calculate_replenishment(part_id, days)
        return self.dc.calculate_all_replenishments(days)
    
    def detect_anomalies(self, days=90):
        return self.ad.detect_all_anomalies(days)
    
    def predict_demand(self, part_id=None, weeks_ahead=4):
        if part_id:
            return self.dp.predict_weekly_demand(part_id, weeks_ahead)
        return self.dp.predict_all_demands(weeks_ahead)
    
    def get_urgent_replenishment(self, weeks_ahead=4):
        return self.dp.get_urgent_replenishment_list(weeks_ahead)

def generate_txt_report(system):
    inventory = system.query_inventory()
    
    anomalies = system.detect_anomalies(days=90)
    
    predictions = system.predict_demand(weeks_ahead=4)
    successful = [p for p in predictions if p['预测状态'] == '成功']
    with_anomalies = [p for p in successful if p['异常提醒']]
    
    urgent = system.get_urgent_replenishment(weeks_ahead=4)
    
    report_lines = []
    
    report_lines.append('=== 配件库存备货提醒系统 ===')
    report_lines.append('')
    
    report_lines.append(' 1. 库存概览')
    report_lines.append(f'   总配件数: {len(inventory)}')
    report_lines.append('')
    
    report_lines.append('  2. 异常检测')
    report_lines.append(f"   库存异常: {len(anomalies['库存异常'])} 个")
    
    for anomaly in anomalies['库存异常']:
        part_id = anomaly['配件ID']
        part_info = next((i for i in inventory if i['配件ID'] == part_id), None)
        if part_info:
            current = part_info['当前库存']
            safety = part_info['安全库存']
            shortage = max(0, safety - current)
            report_lines.append(f"     - {part_id} {part_info['配件名称']}: {anomaly['异常类型']}")
            report_lines.append(f"       现有{current}个, 需求{current + shortage}个, 缺{shortage}个")
    
    report_lines.append('')
    
    report_lines.append('  3. 需求预测 (未来4周)')
    report_lines.append(f'   成功预测: {len(successful)} 个配件')
    report_lines.append(f'   异常提醒: {len(with_anomalies)} 个配件')
    
    for pred in with_anomalies:
        report_lines.append(f"     - {pred['配件ID']}:")
        for alert in pred['异常提醒']:
            z_score = alert.get('Z分数', 0)
            week = alert.get('预测周次', 1)
            report_lines.append(f"       第{week}周需求异常跳升, {z_score:.2f}σ")
    
    report_lines.append('')
    
    report_lines.append('  4. 紧急补货建议')
    report_lines.append(f'   需要紧急补货: {len(urgent)} 个配件')
    
    for item in urgent:
        report_lines.append(f"     - {item['配件ID']}: 缺口={item['缺口']}件")
    
    report_lines.append('')
    report_lines.append('=== 报告生成完成 ===')
    
    return '\n'.join(report_lines)

def main():
    print('=== 配件库存备货提醒系统 ===')
    print(f'运行时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
    
    print('检查数据更新...')
    if check_if_run_today():
        print('开始更新数据...')
        generate_fake_data()
        save_run_date()
        print('数据更新完成！\n')
        system = SparePartsSystem()
    else:
        print('使用现有数据\n')
        system = SparePartsSystem()
    
    report_content = generate_txt_report(system)
    
    output_file = Path('output/report.txt')
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(report_content, encoding='utf-8')
    
    print(report_content)
    print(f'\n报告已保存到: {output_file}')
    print(f'完成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

if __name__ == '__main__':
    main()