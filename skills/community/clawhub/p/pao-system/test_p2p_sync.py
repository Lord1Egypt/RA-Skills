"""测试P2P网络和同步监控模块"""
import asyncio
import sys
sys.path.insert(0, 'src')

from p2p_network import P2PNetworkManager, ConnectionState
from sync_monitor import SyncMonitor, SyncState

async def test():
    print('='*60)
    print('P2P网络模块测试')
    print('='*60)

    p2p = P2PNetworkManager()
    await p2p.start()

    await p2p.connect('peer1', '设备1')
    await p2p.connect('peer2', '设备2')

    status = await p2p.get_status()
    print('连接状态:', status['connections'])

    msg_id = await p2p.send_message('peer1', 'test', {'data': 'hello'})
    print('消息已发送:', msg_id)

    await p2p.stop()
    print('P2P网络测试通过!')

    print()
    print('='*60)
    print('同步监控模块测试')
    print('='*60)

    monitor = SyncMonitor()
    await monitor.start()

    await monitor.on_sync_start('peer1')
    await asyncio.sleep(0.1)
    await monitor.on_sync_complete('peer1', 50.5, 100, 200)

    await monitor.on_sync_start('peer2')
    await asyncio.sleep(0.1)
    await monitor.on_sync_complete('peer2', 30.2, 80, 150)

    await monitor.on_conflict('peer1', 'lww', 'remote_wins')

    full_status = await monitor.get_full_status()
    print('同步状态:', full_status['state'])
    print('指标:', full_status['metrics'])

    await monitor.stop()
    print('同步监控测试通过!')
    print()
    print('='*60)
    print('所有测试通过!')
    print('='*60)

if __name__ == '__main__':
    asyncio.run(test())
