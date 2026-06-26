export class SafetyGatePipeline {
  audit(command: string) {
    const normalized = command.replace(/[\u200B-\u200D\uFEFF]/g, '').trim();
    const results = [
      this.guard('zero-width-unicode', !/[\u200B-\u200D\uFEFF]/.test(command), 'Hidden unicode characters'),
      this.guard('rm-recursive', !/\brm\s+-rf\b/i.test(normalized), 'Recursive deletion'),
      this.guard('del-recursive', !/\bdel\b.*\*|\bRemove-Item\b.*-Recurse/i.test(normalized), 'Recursive delete pattern'),
      this.guard('chmod-777', !/\bchmod\s+777\b/i.test(normalized), 'World-writable permission'),
      this.guard('curl-pipe-shell', !/\bcurl\b.*\|\s*(sh|bash|zsh)/i.test(normalized), 'Remote script execution'),
      this.guard('wget-pipe-shell', !/\bwget\b.*\|\s*(sh|bash|zsh)/i.test(normalized), 'Remote script execution'),
      this.guard('sudo', !/\bsudo\b/i.test(normalized), 'Privilege escalation'),
      this.guard('credential-leak', !/(api[_-]?key|secret|token)\s*=/i.test(normalized), 'Potential secret exposure'),
      this.guard('subshell', !/`.+`|\$\(.+\)/.test(normalized), 'Subshell execution'),
      this.guard('ssh-wildcard', !/\bssh\b.*\*/i.test(normalized), 'Wildcard with SSH'),
      this.guard('zsh-glob-danger', !/[^\s]+\*\*/.test(normalized), 'Potential zsh glob blast radius'),
      this.guard('force-move', !/\b(mv|Move-Item)\b.*-Force/i.test(normalized), 'Forced move'),
      this.guard('git-reset-hard', !/\bgit\s+reset\s+--hard\b/i.test(normalized), 'Hard reset'),
      this.guard('git-clean-force', !/\bgit\s+clean\s+-fdx\b/i.test(normalized), 'Forced git clean')
    ];
    const deny = results.some((r) => !r.passed && ['zero-width-unicode', 'rm-recursive', 'del-recursive', 'curl-pipe-shell', 'wget-pipe-shell', 'git-reset-hard', 'git-clean-force'].includes(r.guard));
    const review = !deny && results.some((r) => !r.passed);
    return { originalCommand: command, normalizedCommand: normalized, decision: deny ? 'deny' : review ? 'review' : 'allow', results };
  }

  countGuards(): number {
    return 14;
  }

  private guard(guard: string, passed: boolean, reason: string) {
    return { guard, passed, reason };
  }
}

export default SafetyGatePipeline;
