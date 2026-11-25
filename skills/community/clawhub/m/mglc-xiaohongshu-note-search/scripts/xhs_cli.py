"""Native command-line entry for each independently packaged skill."""
import argparse
import json
from pathlib import Path
import sys

from xhs_core import Client, XhsError, Job, normalize_plan, call_caps, prices_for, money, read_json, write_json, workspace_lock, execute
from xhs_reports import public_data, render


def main():
    identity = read_json(Path(__file__).with_name('client_identity.json'))
    parser = argparse.ArgumentParser(description=identity['displayName'] + '；使用曼格云小红书接口。')
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--sample-plan', action='store_true', help='输出本技能的计划示例，不联网')
    action.add_argument('--estimate', action='store_true', help='读取实时目录并预估费用，不调用收费接口')
    action.add_argument('--run', action='store_true', help='按明确计划与预算执行')
    action.add_argument('--render', action='store_true', help='从已有数据重新导出，不联网')
    parser.add_argument('--plan', help='UTF-8 JSON 计划文件')
    parser.add_argument('--workspace', help='独立任务输出目录；恢复使用同一目录')
    parser.add_argument('--budget', help='本任务累计 API 预算，单位元')
    parser.add_argument('--yes', action='store_true', help='使用用户已授权的任务范围与预算')
    parser.add_argument('--analysis', help='离线导入含 evidenceIds 的分析 JSON，仅用于 --render')
    args = parser.parse_args()
    try:
        if args.analysis and not args.render:
            raise XhsError('INVALID_ARGUMENT', '--analysis 仅用于 --render。')
        if args.sample_plan:
            print(json.dumps(identity['samplePlan'], ensure_ascii=False, indent=2))
            return 0
        if args.render:
            if not args.workspace:
                raise XhsError('INVALID_ARGUMENT', '--render 需要 --workspace。')
            with workspace_lock(args.workspace):
                data = read_json(Path(args.workspace) / 'data.json')
                if data.get('mode') != identity['mode']:
                    raise XhsError('WORKSPACE_MISMATCH', '工作区来自另一种 Skill。')
                output = render(args.workspace, identity, args.analysis)
            print(json.dumps(output, ensure_ascii=False))
            return 5 if output['quality'] == 'partial' else 0
        if not args.plan:
            raise XhsError('INVALID_ARGUMENT', '需要 --plan；可先用 --sample-plan 查看格式。')
        plan = normalize_plan(identity['mode'], read_json(args.plan))
        if args.run and (not args.workspace or not args.yes or args.budget is None):
            raise XhsError('AUTHORIZATION_REQUIRED', '执行需要 --workspace、--budget 和 --yes；沿用用户已授权的范围即可。')
        budget = money(args.budget) if args.budget is not None else None
        client = Client(identity)
        if args.run and not client.key:
            raise XhsError('API_KEY_REQUIRED', '请在本机环境变量 WM_API_KEY 配置曼格云 API Key。')
        caps = call_caps(identity['mode'], plan)
        prices = prices_for(client.catalog(), caps)
        estimate = {'priceSource': 'customer_catalog' if client.key else 'public_catalog',
                    'calls': [{'operation': k, 'maxCalls': v, 'unitMicros': prices[k]} for k, v in caps.items()],
                    'maximumMicros': sum(prices[k] * v for k, v in caps.items()),
                    'note': '这是指定页数和作品数的调用额度，不保证固定条数；不含模型费用。'}
        if args.estimate:
            print(json.dumps(estimate, ensure_ascii=False, indent=2))
            return 0
        with workspace_lock(args.workspace):
            job = Job(args.workspace, identity['mode'], plan, client, prices, budget)
            result = execute(job, identity['mode'], plan)
            result['estimate'] = estimate
            write_json(Path(args.workspace) / 'data.json', public_data(result))
            delivery = render(args.workspace, identity)
        print(json.dumps({'status': result['status'], 'delivery': delivery,
                          'errors': result['errors'], 'workspace': str(Path(args.workspace).resolve())}, ensure_ascii=False))
        return 5 if result['status'] == 'partial' else 0
    except XhsError as e:
        print(json.dumps({'code': e.code, 'message': e.message, 'retryAfter': e.retry_after}, ensure_ascii=False), file=sys.stderr)
        return 2
    except (OSError, ValueError, TypeError, KeyError):
        print(json.dumps({'code': 'LOCAL_IO_OR_FORMAT_ERROR', 'message': '本地文件、参数或响应格式异常；保留工作区后核对输入。'}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
