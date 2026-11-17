import ConfirmDialog from "/assets/v3/components/confirm_dialog.js";
import AlertDialog from "/assets/v3/components/alert_dialog.js";
import Workflow from "/assets/v3/components/workflow.js"
import {_WF_} from "/assets/v3/components/workflow.js"

export default {
inject:['ibf'],
components:{
    "alert-dialog":AlertDialog,
    "confirm-dialog":ConfirmDialog,
    "workflow":Workflow
},
data() {return {
    service:this.$route.query.service, //ibf本身不是服务，所以需要指定服务名
    flowid:this.$route.query.flow,
    did:this.$route.query.did,
    tags:this.ibf.tags,
    alertDlg:null,
    dtl:[],
    flow:{}//流程定义信息{name,maxStep,steps}
}},
created(){
    _WF_.flowDef(this.flowid).then(fd=>{
        this.flow=fd;
        var segments=this.tags[fd.name]['wfSegs'];
        var dtlUrl=appendParas(fd.dtlApi,{id:this.did});
        request({method:"GET", url:dtlUrl}, this.service).then(resp=>{
            if(resp.code!=RetCode.OK) {
                if(resp.code==RetCode.NOT_EXISTS) {
                    this.removeWf();
                }
                return;
            }
            this.dtl=_WF_.formDtlData(resp.data, segments);
        })
    })
},
mounted(){//不能在created中赋值，更不能在data中
    this.alertDlg=this.$refs.errMsg;
},
methods:{
showDtl() {
    var url=appendParas(this.dtlPage,{id:this.did,flowid:this.flowid,service:this.service});
    this.ibf.goto(url)
},
removeWf() { //数据不存在，工作流数据错乱的情况下，删除工作流记录
    this.$refs.confirmDlg.show(this.tags.wrongFlowState, ()=>{
        _WF_.remove(this.flowid,this.did,this.service).then(resp=>{
            if(resp.code!=RetCode.OK) {
                this.$refs.errMsg.showErr(resp.code, resp.info);
            }else{
                this.ibf.back();
            }
        })
    })
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
    <q-btn flat round icon="arrow_back" dense @click="ibf.back"></q-btn>
    <q-toolbar-title>{{flow.dispName}}</q-toolbar-title>
    <q-btn flat icon="info" @click="showDtl" v-if="dtlPage"></q-btn>
   </q-toolbar>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-sm">
<q-list dense>
  <q-item v-for="d in dtl" dense>
    <q-item-section>{{d.k}}</q-item-section>
    <q-item-section>{{d.v}}</q-item-section>
  </q-item>
</q-list>
<q-separator color="primary" inset></q-separator>
<workflow :service="service" :flowid="flowid" :did="did"
 :flowTags="tags.flowTags" :alertDlg="alertDlg"></workflow>
    </q-page>
  </q-page-container>
</q-layout>
<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></alert-dialog>
<confirm-dialog :title="tags.alert" :close="tags.cancel" :ok="tags.ok" ref="confirmDlg"></confirm-dialog>
`
}