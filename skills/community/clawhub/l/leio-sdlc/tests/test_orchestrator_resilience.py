import os
import sys
import tempfile
import pytest
from unittest.mock import patch, MagicMock

# Add scripts directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

import orchestrator

@pytest.fixture
def mock_workdir():
    with tempfile.TemporaryDirectory() as temp_dir:
        os.makedirs(os.path.join(temp_dir, '.git'))
        yield temp_dir

def test_blast_radius_clears_sessions(mock_workdir):
    # Create some dummy .coder_session files
    session1 = os.path.join(mock_workdir, ".coder_session")
    session2 = os.path.join(mock_workdir, "sub", ".coder_session")
    os.makedirs(os.path.dirname(session2), exist_ok=True)
    
    with open(session1, "w") as f:
        f.write("test_session_1")
    with open(session2, "w") as f:
        f.write("test_session_2")
        
    assert os.path.exists(session1)
    assert os.path.exists(session2)

    # We patch everything so orchestrator main just does blast radius and stops
    with patch('orchestrator.drun') as mock_drun, \
         patch('git_utils.check_git_boundary'), \
         patch('orchestrator.initialize_sandbox'), \
         patch('orchestrator.validate_prd_is_committed'), \
         patch('orchestrator.parse_affected_projects', return_value=[]), \
         patch('sys.argv', ['orchestrator.py', '--workdir', mock_workdir, '--prd-file', 'dummy_prd.md', '--force-replan', 'false', '--channel', 'test-channel', '--test-sleep', '--enable-exec-from-workspace', '--global-dir', mock_workdir]):
         
        def dummy_drun(cmd, *args, **kwargs):
            mock_res = MagicMock()
            if isinstance(cmd, list) and "status" in cmd:
                mock_res.stdout = ""
            elif isinstance(cmd, list) and "branch" in cmd:
                mock_res.stdout = "master\n"
            else:
                mock_res.stdout = ""
            mock_res.returncode = 0
            return mock_res
            
        mock_drun.side_effect = dummy_drun
        
        try:
            orchestrator.main()
        except SystemExit as e:
            assert e.code == 0
            
    assert not os.path.exists(session1)
    assert not os.path.exists(session2)


def test_yellow_path_preserves_session(mock_workdir):
    with patch('orchestrator.teardown_coder_session') as mock_teardown, \
         patch('sys.argv', ['orchestrator.py', '--workdir', mock_workdir, '--prd-file', 'dummy_prd.md', '--force-replan', 'false', '--channel', 'test-channel', '--enable-exec-from-workspace', '--global-dir', mock_workdir]), \
         patch('orchestrator.drun') as mock_drun, \
         patch('orchestrator.dpopen') as mock_dpopen, \
         patch('orchestrator.parse_review_verdict', side_effect=["ACTION_REQUIRED", "APPROVED"]), \
         patch('git_utils.check_git_boundary'), \
         patch('orchestrator.initialize_sandbox'), \
         patch('orchestrator.validate_prd_is_committed'), \
         patch('orchestrator.parse_affected_projects', return_value=[]), \
         patch('orchestrator.safe_git_checkout'), \
         patch('orchestrator.notify_channel'), \
         patch('orchestrator.glob.glob') as mock_glob, \
         patch('orchestrator.set_pr_status'):
         
        def dummy_drun(cmd, *args, **kwargs):
            mock_res = MagicMock()
            if isinstance(cmd, list) and "status" in cmd:
                mock_res.stdout = ""
            elif isinstance(cmd, list) and "branch" in cmd:
                mock_res.stdout = "master\n"
            else:
                mock_res.stdout = ""
            mock_res.returncode = 0
            return mock_res
            
        mock_drun.side_effect = dummy_drun
        
        target_project_name = os.path.basename(os.path.abspath(mock_workdir))
        job_dir = os.path.join(mock_workdir, ".sdlc_runs", target_project_name, "dummy_prd")
        os.makedirs(job_dir, exist_ok=True)
        
        mock_dpopen.return_value.returncode = 0
        # Create a dummy PR file
        pr_file = os.path.join(mock_workdir, "PR_001_test.md")
        with open(pr_file, "w") as f:
            f.write("status: in_progress\n")
            
        def dummy_glob(pattern, recursive=False):
            if ".coder_session" in pattern:
                return []
            return [pr_file]
            
        mock_glob.side_effect = dummy_glob
        
        try:
            # We run max 1 PR to process
            with patch('sys.argv', ['orchestrator.py', '--workdir', mock_workdir, '--prd-file', 'dummy_prd.md', '--force-replan', 'false', '--channel', 'test-channel', '--enable-exec-from-workspace', '--global-dir', mock_workdir, '--max-prs-to-process', '1']):
                orchestrator.main()
        except SystemExit:
            pass
            
        # teardown_coder_session is called when APPROVED (pr_done = True)
        # but during the first iteration (ACTION_REQUIRED), it should NOT be called.
        # Since it only loops once for ACTION_REQUIRED and then APPROVED, it should be called exactly once.
        assert mock_teardown.call_count == 1


def test_red_path_hard_resets(mock_workdir):
    with patch('orchestrator.teardown_coder_session') as mock_teardown, \
         patch('sys.argv', ['orchestrator.py', '--workdir', mock_workdir, '--prd-file', 'dummy_prd.md', '--force-replan', 'false', '--channel', 'test-channel', '--enable-exec-from-workspace', '--global-dir', mock_workdir]), \
         patch('orchestrator.drun') as mock_drun, \
         patch('orchestrator.dpopen') as mock_dpopen, \
         patch('orchestrator.parse_review_verdict', side_effect=["ACTION_REQUIRED", "ACTION_REQUIRED", "ACTION_REQUIRED", "ACTION_REQUIRED", "APPROVED"]), \
         patch('git_utils.check_git_boundary'), \
         patch('orchestrator.initialize_sandbox'), \
         patch('orchestrator.validate_prd_is_committed'), \
         patch('orchestrator.parse_affected_projects', return_value=[]), \
         patch('orchestrator.safe_git_checkout'), \
         patch('orchestrator.notify_channel'), \
         patch('orchestrator.glob.glob') as mock_glob, \
         patch('orchestrator.get_pr_slice_depth', return_value=0), \
         patch('orchestrator.set_pr_status'):
         
        def dummy_drun2(cmd, *args, **kwargs):
            mock_res = MagicMock()
            if isinstance(cmd, list) and "status" in cmd:
                mock_res.stdout = ""
            elif isinstance(cmd, list) and "branch" in cmd:
                mock_res.stdout = "master\n"
            else:
                mock_res.stdout = ""
            mock_res.returncode = 0
            return mock_res
            
        mock_drun.side_effect = dummy_drun2
        
        target_project_name = os.path.basename(os.path.abspath(mock_workdir))
        job_dir = os.path.join(mock_workdir, ".sdlc_runs", target_project_name, "dummy_prd")
        os.makedirs(job_dir, exist_ok=True)
        
        mock_dpopen.return_value.returncode = 0
        # Create a dummy PR file
        pr_file = os.path.join(mock_workdir, "PR_001_test.md")
        with open(pr_file, "w") as f:
            f.write("status: in_progress\n")
            
        def dummy_glob(pattern, recursive=False):
            if ".coder_session" in pattern:
                return []
            if mock_glob.call_count > 5:
                return []
            return [pr_file]
            
        mock_glob.side_effect = dummy_glob
        
        # Simulate arbitrator failure to trigger state_5_trigger
        mock_dpopen.return_value.communicate.return_value = ("REJECTED", "")
        mock_dpopen.return_value.returncode = 1
        
        try:
            with patch('sys.argv', ['orchestrator.py', '--workdir', mock_workdir, '--prd-file', 'dummy_prd.md', '--force-replan', 'false', '--channel', 'test-channel', '--enable-exec-from-workspace', '--global-dir', mock_workdir, '--max-prs-to-process', '1']):
                orchestrator.main()
        except SystemExit:
            pass
            
        # The Red Path triggers teardown_coder_session
        assert mock_teardown.call_count > 0