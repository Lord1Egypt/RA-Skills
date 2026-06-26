/**
 * KubectlFilter - Filter kubectl command output
 */

const BaseFilter = require('./BaseFilter');

class KubectlFilter extends BaseFilter {
  async apply(output, context = {}) {
    if (!this.canFilter(output)) {
      return output;
    }

    output = this.removeAnsiCodes(output);
    const command = context.command || '';

    if (command.includes('get pods') || command.includes('get po')) {
      return this.filterPods(output);
    } else if (command.includes('get services') || command.includes('get svc')) {
      return this.filterServices(output);
    } else if (command.includes('get deploy')) {
      return this.filterDeployments(output);
    } else if (command.includes('get nodes')) {
      return this.filterNodes(output);
    } else if (command.includes('logs')) {
      return this.filterLogs(output);
    } else if (command.includes('describe')) {
      return this.filterDescribe(output);
    }

    return this.filterGeneric(output);
  }

  /**
   * Filter kubectl get pods output
   */
  filterPods(output) {
    const lines = output.split('\n').filter(l => l.trim());
    if (lines.length <= 1) return '☸️ No pods found';

    const pods = lines.slice(1).map(line => {
      const parts = line.split(/\s+/);
      const name = parts[0] || '?';
      const ready = parts[1] || '?';
      const status = parts[2] || '?';
      const statusIcon = status === 'Running' ? '✅' : status === 'Pending' ? '⏳' : '❌';
      return `${statusIcon} ${name} (${ready}) ${status}`;
    });

    const running = pods.filter(p => p.includes('✅')).length;
    const pending = pods.filter(p => p.includes('⏳')).length;
    const failed = pods.filter(p => p.includes('❌')).length;

    const result = [`☸️ ${pods.length} pod(s): ✅${running} ⏳${pending} ❌${failed}`];
    result.push(...pods.slice(0, 10));
    if (pods.length > 10) result.push(`  ... +${pods.length - 10} more`);

    return result.join('\n');
  }

  /**
   * Filter kubectl get services output
   */
  filterServices(output) {
    const lines = output.split('\n').filter(l => l.trim());
    if (lines.length <= 1) return '☸️ No services found';

    const services = lines.slice(1).map(line => {
      const parts = line.split(/\s+/);
      const name = parts[0] || '?';
      const type = parts[1] || '?';
      const clusterIp = parts[2] || '?';
      const ports = parts[4] || '?';
      return `  🔌 ${name} (${type}) ${ports}`;
    });

    return `☸️ ${services.length} service(s):\n${services.join('\n')}`;
  }

  /**
   * Filter kubectl get deployments output
   */
  filterDeployments(output) {
    const lines = output.split('\n').filter(l => l.trim());
    if (lines.length <= 1) return '☸️ No deployments found';

    const deploys = lines.slice(1).map(line => {
      const parts = line.split(/\s+/);
      const name = parts[0] || '?';
      const ready = parts[1] || '?';
      const available = parts[3] || '0';
      const icon = parseInt(available) > 0 ? '✅' : '❌';
      return `${icon} ${name} (${ready})`;
    });

    return `☸️ ${deploys.length} deployment(s):\n${deploys.join('\n')}`;
  }

  /**
   * Filter kubectl get nodes output
   */
  filterNodes(output) {
    const lines = output.split('\n').filter(l => l.trim());
    if (lines.length <= 1) return '☸️ No nodes found';

    const nodes = lines.slice(1).map(line => {
      const parts = line.split(/\s+/);
      const name = parts[0] || '?';
      const status = parts[1] || '?';
      const icon = status === 'Ready' ? '✅' : '❌';
      const version = parts[4] || '?';
      return `${icon} ${name} (${version})`;
    });

    return `☸️ ${nodes.length} node(s):\n${nodes.join('\n')}`;
  }

  /**
   * Filter kubectl logs output
   */
  filterLogs(output) {
    const lines = output.split('\n').filter(l => l.trim());
    if (lines.length === 0) return '📜 No logs';

    const errors = lines.filter(l => /error|exception|fail|panic/i.test(l)).length;
    const warnings = lines.filter(l => /warn/i.test(l)).length;
    const lastLines = lines.slice(-10);

    const result = [`📜 ${lines.length} log lines`];
    if (errors > 0) result.push(`❌ ${errors} errors`);
    if (warnings > 0) result.push(`⚠️  ${warnings} warnings`);
    result.push('');
    result.push('Last 10 lines:');
    result.push(...lastLines.map(l => l.substring(0, 100)));

    return result.join('\n');
  }

  /**
   * Filter kubectl describe output
   */
  filterDescribe(output) {
    const lines = output.split('\n');
    
    // Extract key sections
    const name = lines.find(l => l.startsWith('Name:'))?.replace('Name:', '').trim();
    const namespace = lines.find(l => l.startsWith('Namespace:'))?.replace('Namespace:', '').trim();
    const status = lines.find(l => l.startsWith('Status:'))?.replace('Status:', '').trim();
    const events = lines.filter(l => /Warning|Normal/.test(l)).slice(-5);

    const result = ['☸️ Resource Details'];
    if (name) result.push(`  Name: ${name}`);
    if (namespace) result.push(`  Namespace: ${namespace}`);
    if (status) result.push(`  Status: ${status}`);
    
    if (events.length > 0) {
      result.push('');
      result.push('Recent Events:');
      result.push(...events.map(e => `  ${e.substring(0, 80)}`));
    }

    return result.join('\n');
  }

  /**
   * Generic kubectl filter
   */
  filterGeneric(output) {
    const lines = output.split('\n').filter(l => l.trim());
    if (lines.length <= 15) return output;

    return [
      ...lines.slice(0, 7),
      `[... ${lines.length - 12} lines hidden ...]`,
      ...lines.slice(-5)
    ].join('\n');
  }
}

module.exports = KubectlFilter;
