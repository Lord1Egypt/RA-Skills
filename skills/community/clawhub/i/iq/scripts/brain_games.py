#!/usr/bin/env python3
"""
Brain Games Generator

Generates brain-training games including Sudoku, Tower of Hanoi,
number puzzles, and sliding puzzles.

Usage:
    python brain_games.py --game sudoku|hanoi|magic_square|sliding_puzzle [options]

Examples:
    python brain_games.py --game sudoku --difficulty medium
    python brain_games.py --game hanoi --disks 5
    python brain_games.py --game magic_square --size 3
"""

import argparse
import random
import copy


def generate_sudoku(difficulty="medium"):
    """Generate a Sudoku puzzle with solution."""
    # Difficulty levels control how many cells to remove
    removal_map = {"easy": 35, "medium": 45, "hard": 55}
    cells_to_remove = removal_map.get(difficulty, 45)
    
    # Start with a valid completed grid using backtracking
    def is_valid(board, row, col, num):
        for x in range(9):
            if board[row][x] == num or board[x][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True
    
    def solve(board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for num in nums:
                        if is_valid(board, i, j, num):
                            board[i][j] = num
                            if solve(board):
                                return True
                            board[i][j] = 0
                    return False
        return True
    
    # Generate solution
    solution = [[0]*9 for _ in range(9)]
    solve(solution)
    
    # Create puzzle by removing cells
    puzzle = [row[:] for row in solution]
    removed = 0
    positions = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(positions)
    
    for i, j in positions:
        if removed >= cells_to_remove:
            break
        puzzle[i][j] = 0
        removed += 1
    
    return {"puzzle": puzzle, "solution": solution, "type": "sudoku"}


def generate_hanoi(disks=4):
    """Generate a Tower of Hanoi puzzle with solution."""
    moves = []
    
    def hanoi(n, source, auxiliary, target):
        if n == 1:
            moves.append(f"Move disk 1 from {source} to {target}")
            return
        hanoi(n - 1, source, target, auxiliary)
        moves.append(f"Move disk {n} from {source} to {target}")
        hanoi(n - 1, auxiliary, source, target)
    
    hanoi(disks, "A", "B", "C")
    
    return {
        "type": "tower_of_hanoi",
        "disks": disks,
        "source": "A",
        "auxiliary": "B",
        "target": "C",
        "minimum_moves": len(moves),
        "solution_steps": moves
    }


def generate_magic_square(size=3):
    """Generate a magic square puzzle."""
    if size == 3:
        # 3x3 magic square (Lo Shu)
        base = [[8, 1, 6], [3, 5, 7], [4, 9, 2]]
        magic_sum = 15
    elif size == 4:
        # 4x4 magic square
        base = [
            [16, 3, 2, 13],
            [5, 10, 11, 8],
            [9, 6, 7, 12],
            [4, 15, 14, 1]
        ]
        magic_sum = 34
    else:
        # Generate simple odd-order magic square
        n = size
        magic_sum = n * (n*n + 1) // 2
        base = [[0]*n for _ in range(n)]
        i, j = 0, n // 2
        for num in range(1, n*n + 1):
            base[i][j] = num
            newi, newj = (i - 1) % n, (j + 1) % n
            if base[newi][newj]:
                i += 1
            else:
                i, j = newi, newj
    
    # Create puzzle by removing some numbers
    puzzle = [row[:] for row in base]
    positions = [(i, j) for i in range(size) for j in range(size)]
    random.shuffle(positions)
    to_remove = size * size // 2
    
    for idx, (i, j) in enumerate(positions):
        if idx < to_remove:
            puzzle[i][j] = 0
    
    return {
        "type": "magic_square",
        "size": size,
        "magic_sum": magic_sum,
        "puzzle": puzzle,
        "solution": base
    }


def generate_sliding_puzzle(size=4):
    """Generate a sliding puzzle (15-puzzle style)."""
    # Create solved state
    total = size * size
    solved = list(range(1, total)) + [0]
    board = [solved[i*size:(i+1)*size] for i in range(size)]
    
    # Shuffle by making valid moves from solved state
    empty_pos = (size - 1, size - 1)
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for _ in range(1000):
        di, dj = random.choice(moves)
        ni, nj = empty_pos[0] + di, empty_pos[1] + dj
        if 0 <= ni < size and 0 <= nj < size:
            board[empty_pos[0]][empty_pos[1]], board[ni][nj] = board[ni][nj], board[empty_pos[0]][empty_pos[1]]
            empty_pos = (ni, nj)
    
    return {
        "type": "sliding_puzzle",
        "size": size,
        "puzzle": board,
        "solution": [solved[i*size:(i+1)*size] for i in range(size)],
        "goal": "Arrange numbers 1-15 in order with empty space at bottom-right"
    }


def format_sudoku(data):
    """Format Sudoku as text."""
    puzzle = data["puzzle"]
    solution = data["solution"]
    lines = []
    lines.append("=" * 37)
    lines.append("           SUDOKU PUZZLE")
    lines.append("=" * 37)
    lines.append("\nFill in the grid so that every row,")
    lines.append("every column, and every 3x3 box contains")
    lines.append("the digits 1 through 9.\n")
    
    for i in range(9):
        if i % 3 == 0 and i != 0:
            lines.append("|-------+-------+-------|")
        row_str = "|"
        for j in range(9):
            if j % 3 == 0 and j != 0:
                row_str += "|"
            val = puzzle[i][j]
            row_str += f" {val if val != 0 else ' '} "
        row_str += "|"
        lines.append(row_str)
    lines.append("|-------+-------+-------|")
    
    lines.append("\n--- SOLUTION ---\n")
    for i in range(9):
        if i % 3 == 0 and i != 0:
            lines.append("|-------+-------+-------|")
        row_str = "|"
        for j in range(9):
            if j % 3 == 0 and j != 0:
                row_str += "|"
            row_str += f" {solution[i][j]} "
        row_str += "|"
        lines.append(row_str)
    lines.append("|-------+-------+-------|")
    
    return "\n".join(lines)


def format_hanoi(data):
    """Format Tower of Hanoi as text."""
    lines = []
    lines.append("=" * 50)
    lines.append(f"     TOWER OF HANOI — {data['disks']} DISKS")
    lines.append("=" * 50)
    lines.append("\nRules:")
    lines.append("1. Move only one disk at a time")
    lines.append("2. Only move the top disk of a stack")
    lines.append("3. Never place a larger disk on a smaller disk")
    lines.append(f"\nGoal: Move all disks from {data['source']} to {data['target']}")
    lines.append(f"Minimum moves required: {data['minimum_moves']}")
    lines.append(f"\n--- SOLUTION ({len(data['solution_steps'])} moves) ---\n")
    for i, move in enumerate(data["solution_steps"], 1):
        lines.append(f"{i:3d}. {move}")
    return "\n".join(lines)


def format_magic_square(data):
    """Format magic square as text."""
    size = data["size"]
    puzzle = data["puzzle"]
    solution = data["solution"]
    lines = []
    lines.append("=" * 40)
    lines.append(f"     MAGIC SQUARE — {size}x{size}")
    lines.append("=" * 40)
    lines.append(f"\nFill in the empty cells so that every")
    lines.append(f"row, column, and diagonal sums to {data['magic_sum']}.\n")
    
    width = len(str(size * size)) + 1
    for row in puzzle:
        line = " | ".join(str(x).center(width) if x != 0 else "?".center(width) for x in row)
        lines.append(f"| {line} |")
        lines.append("-" * (len(line) + 4))
    
    lines.append(f"\n--- SOLUTION ---\n")
    for row in solution:
        line = " | ".join(str(x).center(width) for x in row)
        lines.append(f"| {line} |")
        lines.append("-" * (len(line) + 4))
    
    return "\n".join(lines)


def format_sliding_puzzle(data):
    """Format sliding puzzle as text."""
    size = data["size"]
    puzzle = data["puzzle"]
    lines = []
    lines.append("=" * 40)
    lines.append(f"     SLIDING PUZZLE — {size}x{size}")
    lines.append("=" * 40)
    lines.append(f"\n{data['goal']}")
    lines.append("You can slide tiles into the empty space.\n")
    
    width = len(str(size * size - 1)) + 1
    for row in puzzle:
        line = " | ".join(str(x).center(width) if x != 0 else " ".center(width) for x in row)
        lines.append(f"| {line} |")
        lines.append("-" * (len(line) + 4))
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate brain training games")
    parser.add_argument("--game", choices=["sudoku", "hanoi", "magic_square", "sliding_puzzle"],
                        required=True, help="Type of game to generate")
    parser.add_argument("--difficulty", choices=["easy", "medium", "hard"], default="medium",
                        help="Difficulty for Sudoku (default: medium)")
    parser.add_argument("--disks", type=int, default=4, help="Number of disks for Tower of Hanoi (default: 4)")
    parser.add_argument("--size", type=int, default=3, help="Size for magic square or sliding puzzle (default: 3/4)")
    parser.add_argument("--output", help="Output file path (optional)")
    parser.add_argument("--seed", type=int, help="Random seed")
    
    args = parser.parse_args()
    
    if args.seed:
        random.seed(args.seed)
    
    if args.game == "sudoku":
        data = generate_sudoku(args.difficulty)
        output = format_sudoku(data)
    elif args.game == "hanoi":
        data = generate_hanoi(args.disks)
        output = format_hanoi(data)
    elif args.game == "magic_square":
        data = generate_magic_square(args.size)
        output = format_magic_square(data)
    elif args.game == "sliding_puzzle":
        size = args.size if args.size else 4
        data = generate_sliding_puzzle(size)
        output = format_sliding_puzzle(data)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Game saved to: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
