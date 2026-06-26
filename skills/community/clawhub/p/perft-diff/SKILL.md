---
name: perft-diff

description: Finds an incorrect or missing move of user's chess engine by comparing perft results with Stockfish. Use when user reports getting wrong perft results.

metadata:
  openclaw:
    emoji: "♟️"
    requires:
      bins:
        - stockfish
    install:
      - id: apt
        kind: apt
        package: stockfish
        bins:
          - stockfish
        label: Install stockfish (apt)
---



# Perft diff skill



The user's chess engine is generating illegal moves or not generating all legal moves in some position. This is demonstrated by incorrect perft results.



By systematically following the following workflow steps you will end up with a sequence of moves leading to an illegal or a missed move (an anomaly move). The sequence to the anomaly move is your final result you must log to the user.





## Workflow



From the user's commands you must extract the specific test file and test case which demonstrates the perft result mismatch.

From the test case you must extract:

- x = the position's FEN notation

- d = the desired perft depth.



Now you must simply follow this stepwise algorithm:

Let search position be x.

Let remaining depth be d.



1. Log perft from the search position in the user's engine. The test file may include a tool to perform perft logging. You are free to use that or implement your own.



2. Log perft from search position in Stockfish.



3. There is at least one mismatch. Choose any move that has a mismatched result. The search position becomes the search position with your chosen move played. Remaining depth decrements by one.



4. If the remaining depth is 0, stop. Else go to step 1.



5. You now have the move sequence to an anomaly move. Report it to the user and you are done.



There is an example of applying this workflow in practice in {basedir}/example.txt . Inspect it for reference.



# Notes



Important:

- Don't modify the code base apart from the specified test case and possibly creating your own logging tool.



- By systematically following the workflow steps you will end up with a sequence of moves leading to an illegal or a missed move. That is your final result.



- DON'T try to find out why the engine is not working. Just demonstrate that it doesn't work by finding the move sequence leading to a missed or an illegal move.

