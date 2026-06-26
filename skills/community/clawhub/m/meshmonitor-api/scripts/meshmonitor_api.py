#!/usr/bin/env python3
import argparse
import json
import sys
import urllib.parse
import urllib.request


def req(url, token=None, method='GET', body=None):
    headers = {}
    data = None
    if token:
        headers['Authorization'] = f'Bearer {token}'
    if body is not None:
        headers['Content-Type'] = 'application/json'
        data = json.dumps(body).encode('utf-8')
    r = urllib.request.Request(url, headers=headers, method=method, data=data)
    with urllib.request.urlopen(r, timeout=30) as resp:
        return resp.read().decode('utf-8', errors='replace')


def get_json(url, token=None, method='GET', body=None):
    return json.loads(req(url, token=token, method=method, body=body))


def normalize_base(base):
    return base.rstrip('/')


def api_url(base, path):
    return normalize_base(base) + '/api/v1' + path


def docs_js_url(base):
    return normalize_base(base) + '/api/v1/docs/swagger-ui-init.js'


def extract_paths_from_docs(js_text):
    marker = '"paths": {'
    start = js_text.find(marker)
    if start == -1:
        return None
    i = start + len('"paths": ')
    depth = 0
    in_str = False
    esc = False
    out = []
    for ch in js_text[i:]:
        out.append(ch)
        if in_str:
            if esc:
                esc = False
            elif ch == '\\':
                esc = True
            elif ch == '"':
                in_str = False
        else:
            if ch == '"':
                in_str = True
            elif ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    break
    text = ''.join(out)
    try:
        return json.loads(text)
    except Exception:
        return None


def add_query(path, params):
    q = {k: v for k, v in params.items() if v is not None}
    if not q:
        return path
    return path + '?' + urllib.parse.urlencode(q)


def pp(obj):
    print(json.dumps(obj, indent=2))


def cmd_info(args):
    pp(get_json(api_url(args.base_url, '/'), token=args.token))


def cmd_nodes(args):
    path = add_query('/nodes', {
        'active': 'true' if args.active else None,
        'sinceDays': args.since_days,
    })
    pp(get_json(api_url(args.base_url, path), token=args.token))


def cmd_node(args):
    node_id = urllib.parse.quote(args.node_id, safe='!')
    pp(get_json(api_url(args.base_url, f'/nodes/{node_id}'), token=args.token))


def cmd_position_history(args):
    path = add_query(f'/nodes/{urllib.parse.quote(args.node_id, safe="!")}/position-history', {
        'since': args.since,
        'before': args.before,
        'limit': args.limit,
    })
    pp(get_json(api_url(args.base_url, path), token=args.token))


def cmd_channels(args):
    pp(get_json(api_url(args.base_url, '/channels'), token=args.token))


def cmd_channel(args):
    pp(get_json(api_url(args.base_url, f'/channels/{args.channel_id}'), token=args.token))


def cmd_telemetry(args):
    path = add_query('/telemetry', {
        'nodeId': args.node_id,
        'type': args.type,
        'since': args.since,
        'before': args.before,
        'limit': args.limit,
        'offset': args.offset,
    })
    pp(get_json(api_url(args.base_url, path), token=args.token))


def cmd_telemetry_count(args):
    pp(get_json(api_url(args.base_url, '/telemetry/count'), token=args.token))


def cmd_telemetry_node(args):
    path = add_query(f'/telemetry/{urllib.parse.quote(args.node_id, safe="!")}', {
        'type': args.type,
        'since': args.since,
        'before': args.before,
        'limit': args.limit,
        'offset': args.offset,
    })
    pp(get_json(api_url(args.base_url, path), token=args.token))


def cmd_messages(args):
    path = add_query('/messages', {
        'channel': args.channel,
        'fromNodeId': args.from_node_id,
        'toNodeId': args.to_node_id,
        'since': args.since,
        'before': args.before,
        'limit': args.limit,
        'offset': args.offset,
    })
    pp(get_json(api_url(args.base_url, path), token=args.token))


def cmd_message(args):
    pp(get_json(api_url(args.base_url, f'/messages/{urllib.parse.quote(args.message_id, safe="")}'), token=args.token))


def cmd_send_message(args):
    body = {'text': args.text}
    if args.channel is not None:
        body['channel'] = args.channel
    if args.to_node_id is not None:
        body['toNodeId'] = args.to_node_id
    if args.reply_id is not None:
        body['replyId'] = args.reply_id
    pp(get_json(api_url(args.base_url, '/messages'), token=args.token, method='POST', body=body))


def cmd_traceroutes(args):
    path = add_query('/traceroutes', {
        'fromNodeId': args.from_node_id,
        'toNodeId': args.to_node_id,
        'since': args.since,
        'before': args.before,
        'limit': args.limit,
        'offset': args.offset,
    })
    pp(get_json(api_url(args.base_url, path), token=args.token))


def cmd_traceroute(args):
    path = f'/traceroutes/{urllib.parse.quote(args.from_node_id, safe="!")}/{urllib.parse.quote(args.to_node_id, safe="!")}'
    pp(get_json(api_url(args.base_url, path), token=args.token))


def cmd_network(args):
    pp(get_json(api_url(args.base_url, '/network'), token=args.token))


def cmd_topology(args):
    pp(get_json(api_url(args.base_url, '/network/topology'), token=args.token))


def cmd_packets(args):
    path = add_query('/packets', {
        'portnum': args.portnum,
        'channel': args.channel,
        'fromNodeId': args.from_node_id,
        'toNodeId': args.to_node_id,
        'since': args.since,
        'before': args.before,
        'limit': args.limit,
        'offset': args.offset,
    })
    pp(get_json(api_url(args.base_url, path), token=args.token))


def cmd_packet(args):
    pp(get_json(api_url(args.base_url, f'/packets/{args.packet_id}'), token=args.token))


def cmd_solar(args):
    pp(get_json(api_url(args.base_url, '/solar'), token=args.token))


def cmd_solar_range(args):
    path = add_query('/solar/range', {'start': args.start, 'end': args.end})
    pp(get_json(api_url(args.base_url, path), token=args.token))


def cmd_raw(args):
    path = args.path
    if not path.startswith('/'):
        path = '/' + path
    print(req(api_url(args.base_url, path), token=args.token, method=args.method))


def cmd_docs(args):
    js = req(docs_js_url(args.base_url))
    paths = extract_paths_from_docs(js)
    if not paths:
        print('Could not extract paths from docs JS', file=sys.stderr)
        sys.exit(1)
    out = {}
    for path, methods in paths.items():
        out[path] = sorted(methods.keys())
    pp(out)


def cmd_health_summary(args):
    nodes = get_json(api_url(args.base_url, '/nodes'), token=args.token)
    network = get_json(api_url(args.base_url, '/network'), token=args.token)
    messages = get_json(api_url(args.base_url, add_query('/messages', {'limit': args.limit})), token=args.token)
    telemetry = get_json(api_url(args.base_url, '/telemetry/count'), token=args.token)
    data = nodes.get('data', [])
    active = [n for n in data if n.get('lastHeard')]
    favorites = [n for n in data if n.get('isFavorite')]
    out = {
        'summary': {
            'totalNodes': nodes.get('count'),
            'activeNodes': len(active),
            'favoriteNodes': len(favorites),
            'network': network.get('data'),
            'telemetryCount': telemetry.get('count'),
            'recentMessageCount': messages.get('count'),
        },
        'activeNodeNames': [n.get('longName') or n.get('nodeId') for n in active],
        'recentMessages': [
            {
                'from': m.get('fromNodeId'),
                'to': m.get('toNodeId'),
                'text': m.get('text'),
                'timestamp': m.get('timestamp'),
            }
            for m in messages.get('data', [])[:args.limit]
        ]
    }
    pp(out)


def cmd_node_report(args):
    node = get_json(api_url(args.base_url, f'/nodes/{urllib.parse.quote(args.node_id, safe="!")}'), token=args.token)
    telemetry = get_json(api_url(args.base_url, add_query(f'/telemetry/{urllib.parse.quote(args.node_id, safe="!")}', {'limit': args.limit})), token=args.token)
    positions = get_json(api_url(args.base_url, add_query(f'/nodes/{urllib.parse.quote(args.node_id, safe="!")}/position-history', {'limit': args.limit})), token=args.token)
    out = {
        'node': node.get('data'),
        'telemetryCount': telemetry.get('count'),
        'recentTelemetry': telemetry.get('data', [])[:args.limit],
        'positionHistoryCount': positions.get('count'),
        'recentPositions': positions.get('data', [])[:args.limit],
    }
    pp(out)


def cmd_traffic_report(args):
    messages = get_json(api_url(args.base_url, add_query('/messages', {'limit': args.limit})), token=args.token)
    traceroutes = get_json(api_url(args.base_url, add_query('/traceroutes', {'limit': args.limit})), token=args.token)
    out = {
        'messages': messages,
        'traceroutes': traceroutes,
    }
    pp(out)


def cmd_topology_report(args):
    topo = get_json(api_url(args.base_url, '/network/topology'), token=args.token)
    nodes = topo.get('data', {}).get('nodes', [])
    edges = topo.get('data', {}).get('edges', [])
    out = {
        'nodeCount': len(nodes),
        'edgeCount': len(edges),
        'nodes': nodes,
        'edges': edges,
    }
    pp(out)


def main():
    p = argparse.ArgumentParser(description='MeshMonitor API helper')
    p.add_argument('--base-url', required=True)
    p.add_argument('--token')
    sub = p.add_subparsers(dest='cmd', required=True)

    sub.add_parser('info')

    p_nodes = sub.add_parser('nodes')
    p_nodes.add_argument('--active', action='store_true')
    p_nodes.add_argument('--since-days', type=int)

    p_node = sub.add_parser('node')
    p_node.add_argument('node_id')

    p_hist = sub.add_parser('position-history')
    p_hist.add_argument('node_id')
    p_hist.add_argument('--since', type=int)
    p_hist.add_argument('--before', type=int)
    p_hist.add_argument('--limit', type=int)

    sub.add_parser('channels')
    p_channel = sub.add_parser('channel')
    p_channel.add_argument('channel_id', type=int)

    p_tel = sub.add_parser('telemetry')
    p_tel.add_argument('--node-id')
    p_tel.add_argument('--type')
    p_tel.add_argument('--since', type=int)
    p_tel.add_argument('--before', type=int)
    p_tel.add_argument('--limit', type=int)
    p_tel.add_argument('--offset', type=int)

    sub.add_parser('telemetry-count')

    p_tel_node = sub.add_parser('telemetry-node')
    p_tel_node.add_argument('node_id')
    p_tel_node.add_argument('--type')
    p_tel_node.add_argument('--since', type=int)
    p_tel_node.add_argument('--before', type=int)
    p_tel_node.add_argument('--limit', type=int)
    p_tel_node.add_argument('--offset', type=int)

    p_msgs = sub.add_parser('messages')
    p_msgs.add_argument('--channel', type=int)
    p_msgs.add_argument('--from-node-id')
    p_msgs.add_argument('--to-node-id')
    p_msgs.add_argument('--since', type=int)
    p_msgs.add_argument('--before', type=int)
    p_msgs.add_argument('--limit', type=int)
    p_msgs.add_argument('--offset', type=int)

    p_msg = sub.add_parser('message')
    p_msg.add_argument('message_id')

    p_send = sub.add_parser('send-message')
    p_send.add_argument('--channel', type=int)
    p_send.add_argument('--to-node-id')
    p_send.add_argument('--reply-id', type=int)
    p_send.add_argument('text')

    p_trs = sub.add_parser('traceroutes')
    p_trs.add_argument('--from-node-id')
    p_trs.add_argument('--to-node-id')
    p_trs.add_argument('--since', type=int)
    p_trs.add_argument('--before', type=int)
    p_trs.add_argument('--limit', type=int)
    p_trs.add_argument('--offset', type=int)

    p_tr = sub.add_parser('traceroute')
    p_tr.add_argument('from_node_id')
    p_tr.add_argument('to_node_id')

    sub.add_parser('network')
    sub.add_parser('topology')

    p_packets = sub.add_parser('packets')
    p_packets.add_argument('--portnum', type=int)
    p_packets.add_argument('--channel', type=int)
    p_packets.add_argument('--from-node-id')
    p_packets.add_argument('--to-node-id')
    p_packets.add_argument('--since', type=int)
    p_packets.add_argument('--before', type=int)
    p_packets.add_argument('--limit', type=int)
    p_packets.add_argument('--offset', type=int)

    p_packet = sub.add_parser('packet')
    p_packet.add_argument('packet_id')

    sub.add_parser('solar')
    p_sr = sub.add_parser('solar-range')
    p_sr.add_argument('start', type=int)
    p_sr.add_argument('end', type=int)

    p_raw = sub.add_parser('raw')
    p_raw.add_argument('path')
    p_raw.add_argument('--method', default='GET')

    sub.add_parser('docs')

    p_hs = sub.add_parser('health-summary')
    p_hs.add_argument('--limit', type=int, default=10)

    p_nr = sub.add_parser('node-report')
    p_nr.add_argument('node_id')
    p_nr.add_argument('--limit', type=int, default=10)

    p_traf = sub.add_parser('traffic-report')
    p_traf.add_argument('--limit', type=int, default=20)

    sub.add_parser('topology-report')

    args = p.parse_args()
    try:
        {
            'info': cmd_info,
            'nodes': cmd_nodes,
            'node': cmd_node,
            'position-history': cmd_position_history,
            'channels': cmd_channels,
            'channel': cmd_channel,
            'telemetry': cmd_telemetry,
            'telemetry-count': cmd_telemetry_count,
            'telemetry-node': cmd_telemetry_node,
            'messages': cmd_messages,
            'message': cmd_message,
            'send-message': cmd_send_message,
            'traceroutes': cmd_traceroutes,
            'traceroute': cmd_traceroute,
            'network': cmd_network,
            'topology': cmd_topology,
            'packets': cmd_packets,
            'packet': cmd_packet,
            'solar': cmd_solar,
            'solar-range': cmd_solar_range,
            'raw': cmd_raw,
            'docs': cmd_docs,
            'health-summary': cmd_health_summary,
            'node-report': cmd_node_report,
            'traffic-report': cmd_traffic_report,
            'topology-report': cmd_topology_report,
        }[args.cmd](args)
    except Exception as e:
        print(f'ERROR: {e}', file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    main()
