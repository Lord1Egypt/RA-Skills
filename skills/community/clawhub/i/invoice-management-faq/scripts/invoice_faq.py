#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
invoice-management-faq - 发票管理常见问题问答技能

This script provides FAQ query functionality for invoice management procedures.
"""

def query_faq(question: str) -> str:
    """
    Query invoice management FAQ based on user question.
    
    Args:
        question: User's question about invoice management
        
    Returns:
        Standard answer from FAQ
    """
    # 纯FAQ技能，实际问答由主智能体根据SKILL.md直接回答
    # 此脚本预留用于未来扩展批量处理功能
    return f"Please refer to SKILL.md for the complete FAQ list. Question: {question}"

if __name__ == "__main__":
    print("invoice-management-faq skill - please see SKILL.md for usage")
