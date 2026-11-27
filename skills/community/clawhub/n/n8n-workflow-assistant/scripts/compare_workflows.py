"""Compare export structure and changed node keys; never print parameter values."""
import argparse
import hashlib
import json
from pathlib import Path


def load(path):
    value = json.loads(path.read_text(encoding='utf-8-sig'))
    if not isinstance(value, dict) or not isinstance(value.get('nodes'), list):
        raise ValueError('Expected n8n workflow object with nodes')
    return value


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('before', type=Path)
    p.add_argument('after', type=Path)
    a = p.parse_args()
    before, after = load(a.before), load(a.after)
    index = lambda w: {str(n.get('id') or n['name']): n for n in w['nodes']}
    left, right = index(before), index(after)
    changed = []
    for key in sorted(left.keys() & right.keys()):
        keys = sorted(k for k in left[key].keys() | right[key].keys() if left[key].get(k) != right[key].get(k))
        if keys:
            changed.append({'nodeId': key, 'changedKeys': keys})
    def edges(w):
        result = set()
        for source, ports in w.get('connections', {}).items():
            for channel, outputs in ports.items():
                for output, targets in enumerate(outputs):
                    for edge in targets:
                        result.add((source, channel, output, edge['node'], edge.get('type', 'main'), edge.get('index', 0)))
        return result
    le, re = edges(before), edges(after)
    report = {'beforeSha256': hashlib.sha256(a.before.read_bytes()).hexdigest(),
              'afterSha256': hashlib.sha256(a.after.read_bytes()).hexdigest(),
              'addedNodeIds': sorted(right.keys() - left.keys()), 'removedNodeIds': sorted(left.keys() - right.keys()),
              'changedNodes': changed, 'addedConnections': sorted(re - le), 'removedConnections': sorted(le - re),
              'changedTopLevelKeys': sorted(k for k in before.keys() | after.keys()
                                            if k not in {'nodes', 'connections'} and before.get(k) != after.get(k)),
              'parameterValuesIncluded': False}
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
