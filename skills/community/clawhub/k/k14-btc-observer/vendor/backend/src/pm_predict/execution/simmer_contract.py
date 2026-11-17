"""Offline capability contract for a later Simmer PAPER adapter.

Do not call generic SimmerClient.trade() for this strategy without these
semantics. Inspected SDK paper implementation does not preserve them. This
module neither imports the SDK nor discovers credentials or submits requests.
"""
from dataclasses import dataclass
from pm_predict.strategy.parallel_exit import Command


@dataclass(frozen=True)
class PaperCapabilities:
    paper_only: bool
    resting_post_only: bool
    exact_share_limit: bool
    fok_terminal_result: bool
    cancel_fill_fence: bool
    confirmed_fill_ids: bool
    merge_receipts: bool
    durable_outbox_and_inventory: bool
    shared_account_reservations: bool
    snapshot_gate_recheck: bool


REQUIRED = tuple(PaperCapabilities.__dataclass_fields__)

# Observed in public main/client.py on 2026-10-27, source SHA in report.
# False means this contract is not demonstrated, not a claim about every
# unpublished server implementation. The SDK paper trade path prices instant
# fills from mid +/- modeled half-spread and does not forward limit/order_type.
INSPECTED_SIMMER_PAPER = PaperCapabilities(True,False,False,False,False,False,
                                          False,False,False,False)


def compatibility(capabilities=INSPECTED_SIMMER_PAPER):
    missing = [name for name in REQUIRED if not getattr(capabilities,name)]
    return {'ready':not missing,'missing':missing,
            'mode':'PAPER_ONLY','execution_enabled':False,
            'reason':'Native instant paper fills are not a Maker/cancel/FOK/merge simulation' if missing else 'Capability contract met; separate receipt/provenance and durable-outbox integration required'}


def prepare_paper_command(command: Command, capabilities, *, up_is_yes_verified):
    """Normalized adapter request, NOT a call to Simmer trade/batch API.

    Adapters must not use a concurrent batch to make SELL/PAIR atomic. A
    cancellation response alone cannot supply the terminal fill fence.
    """
    if not command.paper_only or not compatibility(capabilities)['ready']:
        raise ValueError('Simmer paper execution blocked: capability contract incomplete')
    if not up_is_yes_verified:
        raise ValueError('market condition/token/Up-Yes mapping must be verified')
    return {'client_command_id':command.id,'market':command.market,'order':command.order,
            'operation':command.kind,'intent':command.reason,
            'outcome':{'Up':'yes','Down':'no',None:None}[command.side],
            'quantity':command.quantity,'limit_price':command.price,
            'time_in_force':command.order_type,'post_only':command.post_only,
            'mode':'PAPER_ONLY','require_live_false':True}
