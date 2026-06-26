# Pentagonal Security Knowledge Base

_Self-healing rules learned from AI pen testing._
_These rules are injected into contract generation prompts when Learning is ON._

---

## Reentrancy Protection
1. Always add reentrancy guards to functions that transfer ETH or tokens
2. Use OpenZeppelin's ReentrancyGuard instead of custom mutex patterns
3. Never allow unchecked external calls in loops
4. Always use ReentrancyGuard with nonReentrant modifier on all functions that make external calls before updating state
5. Implement contract-level reentrancy protection to prevent cross-function reentrancy attacks
6. Update state variables before making external calls (checks-effects-interactions pattern)
7. Never call state-changing functions after external calls that could trigger reentrancy
8. Apply comprehensive reentrancy protection to all state-changing functions, regardless of access control modifiers

## Input Validation
9. Validate all function inputs with require statements before processing
10. Use SafeMath or Solidity 0.8+ checked arithmetic for all calculations
11. Add explicit overflow checks for multiplication operations involving user-controlled values
12. Validate that subtraction operations cannot underflow
13. Set reasonable maximum limits on amounts and rates to prevent overflow

## Access Control
14. Implement access control on all admin functions using OpenZeppelin's Ownable or AccessControl
15. Never use tx.origin for authorization — always use msg.sender
16. Set visibility explicitly on all functions and state variables
17. Implement and verify all access control functions before deploying contracts with role-based permissions

## Gas & DoS Protection
18. Use pull-over-push pattern for ETH transfers to avoid DoS
19. Add array length limits and gas consumption checks to prevent DoS attacks in batch operations
20. Implement maximum array size limits for user-controlled data structures to prevent gas griefing

## Oracle & Price Security
21. Use price oracles with proper validation and manipulation protection
22. Avoid hardcoding external contract addresses that could become deprecated or compromised
23. Use slippage protection with minimum output amounts on all automated swaps

## MEV Protection
24. Avoid predictable and deterministic threshold adjustment mechanisms
25. Protect time-based state transitions from front-running using commit-reveal schemes or randomized delays
26. Implement access controls or rate limiting on functions exploitable through MEV attacks
27. Avoid adjusting contract parameters based on results from external calls that could be manipulated

## State Management
28. Emit events for all state-changing operations
29. Ensure all emergency functions have complete implementations with proper state management
30. Validate that all referenced internal functions are implemented before deployment
31. Implement proper state rollback mechanisms when external calls fail
32. Ensure all state changes are atomic and cannot be partially executed when external calls fail
