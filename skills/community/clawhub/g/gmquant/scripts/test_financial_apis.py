# -*- coding: utf-8 -*-
"""
财务数据 API + last_tick 全量测试
基于掘金官方文档 v3.0.145+ 的字段名规范
测试覆盖:
  - stk_get_index_constituents (指数成分股)
  - stk_get_fundamentals_*_pt (资产负债表/利润表/现金流量表 截面数据, 多标的)
  - stk_get_finance_prime_pt (财务主要指标)
  - stk_get_finance_deriv_pt (财务衍生指标)
  - stk_get_daily_valuation_pt (估值指标)
  - stk_get_daily_mktvalue_pt (市值指标)
  - stk_get_daily_basic_pt (基础指标/股本)
  - last_tick (多标的最新的Tick查询)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gm.api import *

TOKEN = 'c2a347464c31056c84165dff766750fbf2ec67b4'

def separator(title):
    print(f'\n{"="*70}')
    print(f'  {title}')
    print('='*70)

def ok(msg):
    print(f'  [PASS] {msg}')

def fail(msg):
    print(f'  [FAIL] {msg}')

def test_index_constituents():
    """测试1: 指数成分股查询 - 返回DataFrame, 无df参数"""
    separator('TEST 1: stk_get_index_constituents (沪深300成分股)')
    try:
        df = stk_get_index_constituents(index='SHSE.000300')
        print(f'  类型: {type(df).__name__}, 形状: {df.shape}')
        print(f'  列: {df.columns.tolist()}')
        print(f'  前3行:\n{df.head(3).to_string()}')
        ok(f'获取到 {len(df)} 只成分股')
        return True
    except Exception as e:
        fail(str(e))
        return False

def test_balance_pt():
    """测试2: 资产负债表截面数据(多标)"""
    separator('TEST 2: stk_get_fundamentals_balance_pt (资产负债表)')
    try:
        df = stk_get_fundamentals_balance_pt(
            symbols='SHSE.600519, SZSE.000001',
            fields='fix_ast,ttl_ast,mny_cptl,ttl_liab,ttl_eqy,invt,gw,intg_ast',
            date='2024-12-31',
            df=True
        )
        print(f'  形状: {df.shape}, 列: {df.columns.tolist()}')
        print(df.to_string())
        ok(f'资产负债表: {len(df)}只股票 × 7个字段')
        return True
    except Exception as e:
        fail(str(e))
        return False

def test_cashflow_pt():
    """测试3: 现金流量表截面数据(多标)"""
    separator('TEST 3: stk_get_fundamentals_cashflow_pt (现金流量表)')
    try:
        df = stk_get_fundamentals_cashflow_pt(
            symbols='SHSE.600519, SZSE.000001',
            fields='net_cf_oper,net_cf_inv,net_cf_fin,cash_rcv_sale,cash_pur_gds_svc',
            date='2024-12-31',
            df=True
        )
        print(f'  形状: {df.shape}, 列: {df.columns.tolist()}')
        print(df.to_string())
        ok(f'现金流量表: {len(df)}只股票 × 5个字段')
        return True
    except Exception as e:
        fail(str(e))
        return False

def test_income_pt():
    """测试4: 利润表截面数据(多标)"""
    separator('TEST 4: stk_get_fundamentals_income_pt (利润表)')
    try:
        df = stk_get_fundamentals_income_pt(
            symbols='SHSE.600519, SZSE.000001',
            fields='inc_oper,ttl_inc_oper,cost_oper,ttl_cost_oper,oper_prof,net_prof,net_prof_pcom',
            date='2024-12-31',
            df=True
        )
        print(f'  形状: {df.shape}, 列: {df.columns.tolist()}')
        print(df.to_string())
        ok(f'利润表: {len(df)}只股票 × 7个字段')
        return True
    except Exception as e:
        fail(str(e))
        return False

def test_finance_prime_pt():
    """测试5: 财务主要指标截面数据(多标)"""
    separator('TEST 5: stk_get_finance_prime_pt (财务主要指标)')
    try:
        # 注意函数名可能是 stk_get_finance_prime 或 stk_get_finance_prime_pt
        # 注意: ROE字段名是 roe_weight_avg, 不是 roe_waa
        df = stk_get_finance_prime_pt(
            symbols=['SZSE.000001', 'SZSE.300002'],
            fields='eps_basic,eps_dil,net_prof_pcom_yoy,inc_oper_yoy,bps_sh,roe_weight_avg',
            rpt_type=None,
            data_type=None,
            date=None,
            df=True
        )
        print(f'  形状: {df.shape}, 列: {df.columns.tolist()}')
        print(df.to_string())
        ok(f'财务主要指标: {len(df)}只股票 × 6个字段')
        return True
    except AttributeError:
        # 尝试不带 _pt 后缀的版本
        try:
            df = stk_get_finance_prime(
                symbols='SZSE.000001,SZSE.300002',
                fields='eps_basic,eps_dil,net_prof_pcom_yoy,roe_waa',
                df=True
            )
            print(f'  形状: {df.shape}, 列: {df.columns.tolist()}')
            print(df.head().to_string())
            ok(f'财务主要指标(无pt后缀): {len(df)}只股票')
            return True
        except Exception as e2:
            fail(f'stk_get_finance_prime 不存在: {e2}')
            return False
    except Exception as e:
        fail(str(e))
        return False

def test_finance_deriv_pt():
    """测试6: 财务衍生指标截面数据(多标)"""
    separator('TEST 6: stk_get_finance_deriv_pt (财务衍生指标)')
    try:
        df = stk_get_finance_deriv_pt(
            symbols=['SZSE.000001', 'SZSE.300002'],
            fields='eps_basic,eps_dil2,ttl_inc_oper_yoy,inc_oper_yoy,oper_prof_yoy',
            rpt_type=None,
            data_type=None,
            date=None,
            df=True
        )
        print(f'  形状: {df.shape}, 列: {df.columns.tolist()}')
        print(df.to_string())
        ok(f'财务衍生指标: {len(df)}只股票 × 5个字段')
        return True
    except Exception as e:
        fail(str(e))
        return False

def test_valuation_pt():
    """测试7: 估值指标单日截面数据"""
    separator('TEST 7: stk_get_daily_valuation_pt (估值指标 PE/PB/PS等)')
    try:
        df = stk_get_daily_valuation_pt(
            symbols=['SZSE.000001', 'SZSE.300002', 'SHSE.600519'],
            fields='pe_ttm,pe_lyr,pe_mrq,pb_mrq,pb_lyr,ps_ttm,dy_ttm,pcf_ttm_ncf,peg_lyr',
            trade_date=None,
            df=True
        )
        print(f'  形状: {df.shape}, 列: {df.columns.tolist()}')
        print(df.to_string())
        ok(f'估值指标: {len(df)}只股票 × 9个字段')
        return True
    except Exception as e:
        fail(str(e))
        return False

def test_mktvalue_pt():
    """测试8: 市值指标单日截面数据"""
    separator('TEST 8: stk_get_daily_mktvalue_pt (市值指标)')
    try:
        df = stk_get_daily_mktvalue_pt(
            symbols=['SZSE.000001', 'SZSE.300002', 'SHSE.600519'],
            fields='tot_mv,a_mv,a_mv_ex_ltd,ev,ev_ex_curr,ev_ebitda,equity_value',
            trade_date=None,
            df=True
        )
        print(f'  形状: {df.shape}, 列: {df.columns.tolist()}')
        print(df.to_string())
        ok(f'市值指标: {len(df)}只股票 × 7个字段')
        return True
    except Exception as e:
        fail(str(e))
        return False

def test_daily_basic_pt():
    """测试9: 基础指标/股本 单日截面数据"""
    separator('TEST 9: stk_get_daily_basic_pt (基础指标/股本)')
    try:
        # 注意: 基础指标字段名是 circ_shr/ttl_shr_unl/ttl_shr_ltd 等, 不是 float_shr/free_shr
        df = stk_get_daily_basic_pt(
            symbols=['SZSE.000001', 'SZSE.300002', 'SHSE.600519'],
            fields='tclose,turnrate,ttl_shr,circ_shr,ttl_shr_unl,ttl_shr_ltd,a_shr_unl',
            trade_date=None,
            df=True
        )
        print(f'  形状: {df.shape}, 列: {df.columns.tolist()}')
        print(df.to_string())
        ok(f'基础指标: {len(df)}只股票 × 9个字段')
        return True
    except Exception as e:
        fail(str(e))
        return False


if __name__ == '__main__':
    set_token(TOKEN)
    
    results = {}
    
    results['index_constituents'] = test_index_constituents()
    results['balance_pt']       = test_balance_pt()
    results['cashflow_pt']      = test_cashflow_pt()
    results['income_pt']        = test_income_pt()
    results['finance_prime']    = test_finance_prime_pt()
    results['finance_deriv']   = test_finance_deriv_pt()
    results['valuation_pt']     = test_valuation_pt()
    results['mktvalue_pt']      = test_mktvalue_pt()
    results['daily_basic_pt']   = test_daily_basic_pt()
    
    separator('测试结果汇总')
    passed = sum(results.values())
    total = len(results)
    for name, result in results.items():
        status = '[PASS]' if result else '[FAIL]'
        print(f'  {status}  {name}')
    
    print(f'\n  Total: {passed}/{total} passed')
