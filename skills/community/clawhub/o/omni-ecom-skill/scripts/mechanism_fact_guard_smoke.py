import unittest
from mechanism_fact_guard import validate


class MechanismTests(unittest.TestCase):
    def setUp(self):
        self.package={'client_scope':'runtime-acceptance-no-client-data','report_inventory':{'report_count':1},'claim_ledger':{'claims':[]}}

    def test_actual_structural_count_is_not_sales(self):
        fact={'id':'F','claim':'report_count 为 1，非客户经营数据。'}
        self.assertEqual(validate([fact],self.package)[0]['value'],1)
        self.assertIn('1',fact['claim'])

    def test_false_count_is_blocked(self):
        with self.assertRaisesRegex(ValueError,'count_mismatch'):
            validate([{'claim':'report_count=2'}],self.package)

    def test_unbound_cost_is_still_blocked(self):
        with self.assertRaisesRegex(ValueError,'binding_mismatch'):
            validate([{'claim':'report_count=1；推广花费500元。'}],self.package)

    def test_business_scope_cannot_use_count_exemption(self):
        self.package['client_scope']='customer'
        with self.assertRaisesRegex(ValueError,'not_authorized'):
            validate([{'claim':'report_count=1'}],self.package)

    def test_unbound_economic_count_without_unit_still_blocks(self):
        with self.assertRaisesRegex(ValueError,'binding_mismatch'):
            validate([{'claim':'CSV 字段显示销售金额 500。'}],self.package)

    def test_hashes_and_row_counts_remain_mechanism_observations(self):
        validate([{'claim':'CSV 共 1 行、11 列，文件 219 字节，SHA256='+'a'*64}],self.package)


if __name__=='__main__': unittest.main()
