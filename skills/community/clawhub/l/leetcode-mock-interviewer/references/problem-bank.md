# Problem Bank

Example problems by topic and difficulty for inspiration. This list is **not exhaustive** — any LeetCode problem is valid for mock interviews. Use these as a starting point when you need quick selection.

## Array

| Difficulty | Problem | Key Technique |
|------------|---------|---------------|
| Easy | Two Sum | Hash map lookup |
| Easy | Best Time to Buy and Sell Stock | Single pass, track min |
| Medium | 3Sum | Sort + two pointers |
| Medium | Product of Array Except Self | Prefix/suffix products |
| Medium | Container With Most Water | Two pointers |
| Hard | First Missing Positive | Index-as-hash |
| Hard | Trapping Rain Water | Two pointers or stack |

## String

| Difficulty | Problem | Key Technique |
|------------|---------|---------------|
| Easy | Valid Anagram | Frequency count |
| Easy | Valid Palindrome | Two pointers |
| Medium | Longest Substring Without Repeating Characters | Sliding window + set |
| Medium | Group Anagrams | Sorted key hashing |
| Medium | Longest Palindromic Substring | Expand around center / DP |
| Hard | Minimum Window Substring | Sliding window + frequency map |

## Hash Table

| Difficulty | Problem | Key Technique |
|------------|---------|---------------|
| Easy | Contains Duplicate | Set membership |
| Easy | Ransom Note | Character frequency |
| Medium | Top K Frequent Elements | Bucket sort or heap |
| Medium | Subarray Sum Equals K | Prefix sum + hash map |

## Two Pointers

| Difficulty | Problem | Key Technique |
|------------|---------|---------------|
| Easy | Remove Duplicates from Sorted Array | Fast/slow pointers |
| Medium | Sort Colors | Dutch national flag |
| Medium | 4Sum | Sort + nested two pointers |

## Sliding Window

| Difficulty | Problem | Key Technique |
|------------|---------|---------------|
| Medium | Longest Repeating Character Replacement | Window + max freq |
| Medium | Permutation in String | Fixed-size window + freq |
| Hard | Sliding Window Maximum | Monotonic deque |

## Stack / Queue

| Difficulty | Problem | Key Technique |
|------------|---------|---------------|
| Easy | Valid Parentheses | Stack matching |
| Medium | Daily Temperatures | Monotonic stack |
| Medium | Evaluate Reverse Polish Notation | Stack evaluation |
| Hard | Largest Rectangle in Histogram | Monotonic stack |

## Linked List

| Difficulty | Problem | Key Technique |
|------------|---------|---------------|
| Easy | Reverse Linked List | Iterative pointer swap |
| Easy | Merge Two Sorted Lists | Dummy head + merge |
| Medium | Add Two Numbers | Carry propagation |
| Medium | LRU Cache | Hash map + doubly linked list |
| Hard | Merge K Sorted Lists | Min-heap or divide and conquer |

## Tree

| Difficulty | Problem | Key Technique |
|------------|---------|---------------|
| Easy | Maximum Depth of Binary Tree | DFS recursion |
| Easy | Invert Binary Tree | Recursive swap |
| Medium | Binary Tree Level Order Traversal | BFS queue |
| Medium | Validate Binary Search Tree | In-order bounds |
| Medium | Lowest Common Ancestor of BST | BST property split |
| Hard | Binary Tree Maximum Path Sum | Post-order with global max |
| Hard | Serialize and Deserialize Binary Tree | BFS/DFS + delimiter |

## Graph

| Difficulty | Problem | Key Technique |
|------------|---------|---------------|
| Medium | Number of Islands | BFS/DFS flood fill |
| Medium | Clone Graph | BFS/DFS + visited map |
| Medium | Course Schedule | Topological sort (Kahn or DFS) |
| Medium | Pacific Atlantic Water Flow | Multi-source BFS/DFS |
| Hard | Word Ladder | BFS shortest path |
| Hard | Alien Dictionary | Topological sort |

## Binary Search

| Difficulty | Problem | Key Technique |
|------------|---------|---------------|
| Easy | Binary Search | Classic template |
| Medium | Search in Rotated Sorted Array | Modified binary search |
| Medium | Find Minimum in Rotated Sorted Array | Binary search on rotation |
| Hard | Median of Two Sorted Arrays | Binary search on partition |

## Dynamic Programming

| Difficulty | Problem | Key Technique |
|------------|---------|---------------|
| Easy | Climbing Stairs | Fibonacci DP |
| Medium | Coin Change | Unbounded knapsack |
| Medium | Longest Increasing Subsequence | DP or patience sort |
| Medium | Word Break | DP + set lookup |
| Medium | House Robber | Linear DP with skip |
| Hard | Edit Distance | 2D DP |
| Hard | Regular Expression Matching | 2D DP |
| Hard | Burst Balloons | Interval DP |

## Greedy

| Difficulty | Problem | Key Technique |
|------------|---------|---------------|
| Medium | Jump Game | Track max reachable |
| Medium | Gas Station | Net surplus scan |
| Medium | Task Scheduler | Greedy + idle slots |
| Hard | Candy | Two-pass greedy |

## Backtracking

| Difficulty | Problem | Key Technique |
|------------|---------|---------------|
| Medium | Subsets | Include/exclude recursion |
| Medium | Permutations | Swap or visited set |
| Medium | Combination Sum | DFS with remainder |
| Hard | N-Queens | Column/diagonal constraint |
| Hard | Word Search II | Trie + DFS |

## Heap / Priority Queue

| Difficulty | Problem | Key Technique |
|------------|---------|---------------|
| Medium | Kth Largest Element in an Array | Quickselect or min-heap |
| Medium | Task Scheduler | Max-heap + cooldown |
| Hard | Find Median from Data Stream | Two heaps |
| Hard | Merge K Sorted Lists | Min-heap |

## Trie

| Difficulty | Problem | Key Technique |
|------------|---------|---------------|
| Medium | Implement Trie | Node children map |
| Medium | Design Add and Search Words | Trie + DFS wildcard |
| Hard | Word Search II | Trie + backtracking |

## Union Find

| Difficulty | Problem | Key Technique |
|------------|---------|---------------|
| Medium | Number of Connected Components | Union-Find with rank |
| Medium | Redundant Connection | Cycle detection via union |
| Hard | Accounts Merge | Union-Find + email mapping |

## MLE / AI Engineer Additions

For MLE/AI Engineer roles, also consider these system-design-adjacent coding problems:

| Difficulty | Problem | Key Technique |
|------------|---------|---------------|
| Medium | Implement Matrix Multiplication | Nested loops, optimization |
| Medium | Sparse Matrix Multiplication | Skip zeros |
| Medium | Design Hit Counter | Queue or circular buffer |
| Hard | Design Search Autocomplete System | Trie + priority queue |
| Hard | Implement LFU Cache | Hash map + doubly linked list + freq map |

## Selection Strategy

1. **Random**: pick uniformly from the candidate's chosen difficulty across all topics.
2. **Topic-specific**: pick from the matching topic table.
3. **Rapid-fire**: pick 3 easy/medium problems from different topics for variety.
4. **Weakness drill**: if a candidate mentions a weak area, pick 2-3 problems from that topic at increasing difficulty.
