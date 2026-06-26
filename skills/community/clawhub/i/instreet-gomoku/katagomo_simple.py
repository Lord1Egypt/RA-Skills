# -*- coding: utf-8 -*-
"""
KataGomo 桥接器 - 修复坐标问题 v6.2
修复 GTP 协议中 I 列被跳过的问题
"""
import subprocess
import os
import re

KATAGOMO_DIR = r"D:\Games\KataGomo"

# KataGomo GTP 列映射 (I 被跳过)
# InStreet: A B C D E F G H I J K L M N O (15列)
# KataGomo: A B C D E F G H J K L M N O P (15列，I被跳过)
# 转换: I->J, J->K, K->L, L->M, M->N, N->O, O->P

def to_katagomo_coord(coord):
    """将 InStreet 坐标转换为 KataGomo 坐标"""
    if not coord:
        return coord
    col = coord[0].upper()
    row = coord[1:]
    
    # 如果列是 I 或之后，需要偏移
    if col >= 'I':
        # ord('I') = 73, ord('J') = 74
        new_col = chr(ord(col) + 1)
        return new_col + row
    return coord

def from_katagomo_coord(coord):
    """将 KataGomo 坐标转换回 InStreet 坐标"""
    if not coord:
        return coord
    col = coord[0].upper()
    row = coord[1:]
    
    # 如果列是 J 或之后，需要回退
    if col >= 'J':
        new_col = chr(ord(col) - 1)
        return new_col + row
    return coord


class KataGomo:
    """KataGomo 引擎调用"""
    
    @staticmethod
    def get_best_move(board_str, my_color):
        """
        获取最佳落子
        board_str: InStreet 棋盘字符串
        my_color: 'black' 或 'white'
        返回: (x, y, position, reason)
        """
        # 解析棋盘获取历史着法
        moves = []
        if board_str:
            lines = board_str.strip().split('\n')
            for line in lines:
                line = line.strip()
                # 跳过表头行 (A B C D...)
                if not line or line[0] in 'ABCDEFGHIJ':
                    continue
                parts = line.split()
                if len(parts) < 2:
                    continue
                try:
                    row = int(parts[0]) - 1
                except:
                    continue
                # 正确解析: parts[0]=行号, parts[1]=A列, parts[2]=B列, ...
                for col in range(15):
                    if col + 1 >= len(parts):
                        break
                    cell = parts[col + 1]
                    if cell in ['X', 'O']:
                        color = 'black' if cell == 'X' else 'white'
                        col_letter = chr(ord('A') + col)
                        # 不转换！InStreet 的列号直接对应 KataGomo
                        # 只需要发送时处理 GTP 的 I 列问题
                        move = f"{col_letter}{row + 1}"
                        moves.append((color, move))
        
        # 构建 GTP 命令 - 需要转换坐标!
        gtp_cmds = ["boardsize 15", "clear_board"]
        for color, move in moves:
            # 转换坐标：InStreet -> KataGomo
            kg_move = to_katagomo_coord(move)
            gtp_cmds.append(f"play {color} {kg_move}")
        
        # AI 思考
        kg_color = my_color
        gtp_cmds.append(f"genmove {kg_color}")
        gtp_cmds.append("quit")
        
        # 创建临时命令文件
        cmd_file = os.path.join(KATAGOMO_DIR, "temp_commands.txt")
        with open(cmd_file, 'w') as f:
            f.write('\n'.join(gtp_cmds))
        
        # 执行 - 使用 FREESTYLE（无禁手）规则
        engine = os.path.join(KATAGOMO_DIR, "engine", "gom15x_trt.exe")
        config = os.path.join(KATAGOMO_DIR, "engine.cfg")
        model = os.path.join(KATAGOMO_DIR, "model.bin")
        
        print(f"[KataGomo] Engine: {engine}")
        print(f"[KataGomo] Moves: {moves}")
        print(f"[KataGomo] Requesting genmove {kg_color}")
        
        try:
            with open(cmd_file, 'r') as fin:
                proc = subprocess.Popen(
                    [engine, "gtp", "-config", config, "-model", model, "-override-config", "basicRule=FREESTYLE"],
                    stdin=fin,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    cwd=KATAGOMO_DIR,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                )
                output, _ = proc.communicate(timeout=120)
            
            output_str = output.decode('utf-8', errors='replace')
            print(f"[KataGomo] Output (last 500 chars): {output_str[-500:]}")
            
            # 解析输出找着法
            lines = output_str.split('\n')
            best_move = None
            
            for i, line in enumerate(lines):
                line = line.strip()
                if '=' in line:
                    parts = line.split('=', 1)
                    if len(parts) > 1:
                        move = parts[1].strip()
                        if move and re.match(r'^[A-P]\d{1,2}$', move):
                            best_move = move
                            print(f"[KataGomo] Found move: {move}")
                            break
                        elif move == '' and i + 1 < len(lines):
                            next_line = lines[i + 1].strip()
                            if re.match(r'^[A-P]\d{1,2}$', next_line):
                                best_move = next_line
                                print(f"[KataGomo] Found move (next line): {best_move}")
                                break
            
            if best_move:
                # 转换坐标回 InStreet 格式
                inStreet_move = from_katagomo_coord(best_move)
                
                col = ord(inStreet_move[0].upper()) - ord('A')
                try:
                    row = int(inStreet_move[1:]) - 1
                except:
                    return None, None, None, f"无效着法: {inStreet_move}"
                
                reasoning = "KataGomo AI 深度计算"
                print(f"[KataGomo] Returning: {inStreet_move} ({col}, {row}) from {best_move}")
                return col, row, inStreet_move, reasoning
            
            print(f"[KataGomo] No move found in output")
            return None, None, None, "未找到着法"
            
        except subprocess.TimeoutExpired:
            print("[KataGomo] Timeout!")
            return None, None, None, "超时"
        except Exception as e:
            print(f"[KataGomo] Error: {e}")
            return None, None, None, str(e)
        finally:
            try:
                os.remove(cmd_file)
            except:
                pass


if __name__ == "__main__":
    # 测试坐标转换
    print("Testing coordinate conversion:")
    test_coords = ["H8", "I8", "J8", "K8", "L8"]
    for c in test_coords:
        kg = to_katagomo_coord(c)
        back = from_katagomo_coord(kg)
        print(f"  {c} -> KataGomo: {kg} -> Back: {back}")
