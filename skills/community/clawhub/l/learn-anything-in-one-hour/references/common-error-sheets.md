# Common Error Cheat Sheets

## Python Beginner Errors
| Error | Fix |
|-------|-----|
| SyntaxError: invalid syntax | Check for missing colons after if/for/def lines, unmatched quotes/parentheses |
| NameError: name 'x' is not defined | You used a variable before creating it, or misspelled the variable name |
| IndentationError | Python uses indentation for blocks - make sure lines in the same block are indented the same amount |
| TypeError: can only concatenate str (not "int") to str | Convert numbers to strings with str() before adding them to text |
| IndexError: list index out of range | You're trying to access a position in a list that doesn't exist (remember lists start at 0) |

## Git Common Errors
| Error | Fix |
|-------|-----|
| fatal: not a git repository | Run git init in your folder first, or cd to the correct folder that has a .git directory |
| error: src refspec main does not match any | You haven't made any commits yet before pushing - run git add . && git commit -m "first commit" first |
| fatal: Authentication failed | Double check your Git credentials, or make sure you have access to the remote repo |
| error: failed to push some refs to ... | Someone else pushed changes before you - run git pull first to merge their changes |
| merge conflict | Open the conflicting file, edit to remove the <<< >>> conflict markers, then git add and commit again |
